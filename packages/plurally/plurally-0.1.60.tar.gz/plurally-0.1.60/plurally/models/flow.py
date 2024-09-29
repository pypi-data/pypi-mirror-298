import uuid
from collections import defaultdict
from copy import deepcopy
from typing import Any, Dict, List, Union, get_origin

from loguru import logger
from pydantic import BaseModel, create_model

from plurally import models
from plurally.json_utils import replace_refs
from plurally.models import utils
from plurally.models.node import Node
from plurally.models.source.constant import ConstantSource


def is_list_type(schema):
    return hasattr(schema, "annotation") and get_origin(schema.annotation) is list


class Flow:
    def __init__(self, name: str = "") -> None:
        global nx
        import networkx as nx

        self._flow_id = f"fl-{str(uuid.uuid4())}"
        self.name = name
        self.graph = nx.MultiDiGraph()

    def __contains__(self, node: Node):
        assert isinstance(node, Node)
        return node in self.graph

    def get_scopes_and_meta_data(self):
        scopes_and_meta_data = []
        for node in self.graph.nodes:
            node_scopes_and_meta_data = node.get_scopes_and_meta_data()
            node_scopes = node_scopes_and_meta_data[0]
            if node_scopes:
                scopes_and_meta_data.append(node_scopes_and_meta_data)
        return scopes_and_meta_data

    def add_node(
        self,
        node: Node,
    ) -> Node:
        if node in self:
            raise ValueError(f"Block with id={node.node_id[:7]} already registered")
        if node.IS_TRIGGER:
            if any([n.IS_TRIGGER for n in self.graph.nodes]):
                raise ValueError("Flow can only have one trigger block")
        self.graph.add_node(node)
        return node

    def get_node(self, node_id: str) -> Node:
        for node in self.graph.nodes:
            if node.node_id == node_id:
                return node
        raise ValueError(f"Node with {node_id=} not found")

    def connect_nodes(
        self,
        src_node: Union[str, "Node"],
        src_handle: str,
        tgt_node: Union[str, "Node"],
        tgt_handle: str,
    ):
        """Connect this node's output to another node's input."""
        if isinstance(src_node, str):
            src_node = self.get_node(src_node)
        if isinstance(tgt_node, str):
            tgt_node = self.get_node(tgt_node)

        if src_node is tgt_node:
            raise ValueError(f"Cannot connect node with itself: {src_node}")

        outputs_annots = src_node.OutputSchema.model_fields
        if src_handle not in outputs_annots:
            raise ValueError(
                f"Output {src_handle} not found in node {src_node}, options are {list(outputs_annots)}"
            )
        for node in (src_node, tgt_node):
            if node not in self:
                raise ValueError(f"{node} was not added to {self}")

        inputs_annots = tgt_node.InputSchema.model_fields
        if tgt_handle not in inputs_annots:
            raise ValueError(
                f"Input {tgt_handle} not found in node {tgt_node}, options are {list(inputs_annots)}"
            )

        # if tgt_handle is not a list and there already is a connection it is False
        if not is_list_type(inputs_annots[tgt_handle]):
            for src, tgt, key in self.graph.in_edges(tgt_node, data=True):
                if key["tgt_handle"] == tgt_handle:
                    raise ValueError(
                        f"Node {tgt_node.name} already has a connection for {tgt_handle}"
                    )

        if not tgt_node.validate_connection(src_node, src_handle, tgt_handle):
            raise ValueError(f"Connection between {src_node} and {tgt_node} is invalid")

        key = f"{src_handle}###{tgt_handle}"
        if (src_node, tgt_node, key) in self.graph.edges:
            raise ValueError(
                f"Connection between {src_node} and {tgt_node} with {src_handle=} and {tgt_handle=} already exists"
            )

        self.graph.add_edge(
            src_node,
            tgt_node,
            src_handle=src_handle,
            tgt_handle=tgt_handle,
            key=key,
        )

    def disconnect_nodes(
        self,
        src_node: Union[str, "Node"],
        src_handle: str,
        tgt_node: Union[str, "Node"],
        tgt_handle: str,
    ):
        """Disconnect this node connection."""
        if isinstance(src_node, str):
            src_node = self.get_node(src_node)
        if isinstance(tgt_node, str):
            tgt_node = self.get_node(tgt_node)
        if src_node is tgt_node:
            raise ValueError(f"Cannot connect node with itself: {src_node}")
        try:
            self.graph.remove_edge(
                src_node, tgt_node, key=f"{src_handle}###{tgt_handle}"
            )
        except nx.NetworkXError:
            raise ValueError(
                f"Connection between {src_node} and {tgt_node} with {src_handle=} and {tgt_handle=} not found"
            )

    def delete_node(self, node: Union[str, "Node"]):
        """Remove a node from the flow."""
        if isinstance(node, str):
            node = self.get_node(node)
        self.graph.remove_node(node)

    def run_callbacks(self, items):
        for item in items:
            item.callback()

    def __call__(self, output_overrides: Dict[str, BaseModel] = None) -> Any:
        state = self.states()

        try:
            output_overrides = output_overrides if output_overrides else {}
            if output_overrides:
                logger.debug(f"Will override for nodes: {','.join(output_overrides)}")
            no_run = set()

            sorted_nodes = list(nx.topological_sort(self.graph))
            trigger_ix = None
            for item in sorted_nodes:
                if isinstance(item, Node) and item.IS_TRIGGER:
                    trigger_ix = item

                if not isinstance(item, Node):
                    break

                if isinstance(item, ConstantSource):
                    # constant source always have outputs and it is not reset at every iteration
                    continue

                item.outputs = {}

            assert trigger_ix, "Flow must have a trigger block"

            # make sure trigger block is the first one
            # this will make sure that the flow is immediatlly aborted if the trigger node has no outputs
            sorted_nodes.remove(trigger_ix)
            sorted_nodes = [trigger_ix] + sorted_nodes

            for item in sorted_nodes:
                try:
                    if not isinstance(item, Node):
                        break
                    kwargs = {}
                    for src_node, tgt_node, attrs in self.graph.in_edges(item, True):
                        src_handle = attrs["src_handle"]
                        tgt_handle = attrs["tgt_handle"]

                        src_value = src_node.outputs.get(src_handle)
                        # if it is a list, it should append
                        if is_list_type(tgt_node.InputSchema.model_fields[tgt_handle]):
                            if tgt_handle not in kwargs:
                                kwargs[tgt_handle] = []
                            kwargs[tgt_handle].append(src_value)
                        else:
                            kwargs[tgt_handle] = src_value
                        logger.debug(f"Processing {src_node} -> {tgt_node}")

                    node_overrides = output_overrides.get(item.node_id)
                    if node_overrides:
                        logger.debug(f"Overriding execution of {item}")
                        item.outputs = node_overrides.model_dump()
                    else:
                        parent_no_run = item in no_run
                        is_no_run = not kwargs.get("run", True)
                        if parent_no_run or is_no_run:
                            if parent_no_run:
                                logger.debug(
                                    f"Skipping {item} - parent was marked as no_run"
                                )
                            if is_no_run:
                                logger.debug(f"Skipping {item} - run is set to False")
                            for node in self.graph.successors(item):
                                no_run.add(node)
                            continue

                        logger.debug(f"Forwarding {item} with {list(kwargs)}")
                        item(**kwargs)
                        if item.outputs is None:
                            logger.debug(f"Node {item} has no outputs")
                        else:
                            logger.debug(
                                f"Finished {item}, outputs: {list(item.outputs) if item.outputs else None}"
                            )

                        if item.IS_TRIGGER and item.outputs is None:
                            # skip if trigger has no outputs
                            logger.debug(
                                f"Aborting execution due to missing outputs from {item}"
                            )
                            self.run_callbacks(sorted_nodes)
                            return

                except Exception as e:
                    logger.exception(e)
                    raise RuntimeError(
                        f"{type(item).__name__} [{item.name} (id={item.node_id[:7]})]\nfailed: {e}"
                    ) from e

            self.run_callbacks(sorted_nodes)

        except Exception:
            self.update(state)
            raise

    def __str__(self) -> str:
        return f"{type(self).__name__}(name={self.name}, id={self._flow_id[:4]})"

    def serialize(self) -> Dict:
        output_schemas, input_schemas = {}, {}

        for node in self.graph.nodes:
            input_schemas[node.node_id] = replace_refs(
                node.InputSchema.model_json_schema()
            )
            output_schemas[node.node_id] = replace_refs(
                node.OutputSchema.model_json_schema()
            )

        s = nx.node_link_data(self.graph)
        s["nodes"] = [{**n, "id": n["id"].serialize()} for n in s["nodes"]]

        links = []
        for link in s["links"]:
            source = link["source"]
            target = link["target"]

            src_handle_title = output_schemas[source.node_id]["properties"][
                link["src_handle"]
            ].get("title")
            tgt_handle_title = input_schemas[target.node_id]["properties"][
                link["tgt_handle"]
            ].get("title")

            label = f"{src_handle_title} -> {tgt_handle_title}"
            links.append(
                {
                    **link,
                    "label": label,
                    "source": source.node_id,
                    "target": target.node_id,
                }
            )
        s["links"] = links
        return s

    def states(self) -> Dict[str, Dict]:
        return {node.node_id: node.state() for node in self.graph.nodes}

    def update(self, state: Dict[str, Dict]):
        for node in self.graph.nodes:
            state_update = state.get(node.node_id)
            if state_update:
                for key, value in state_update.items():
                    assert hasattr(
                        node, key
                    ), f"Node {node} does not have attribute {key}"
                    assert key in node.STATES
                    setattr(node, key, value)

    @classmethod
    def parse(cls, data: Dict) -> "Flow":
        global nx
        import networkx as nx

        data = deepcopy(data)

        flow = cls()
        nodes = {}
        nodes_list = []
        for n in data["nodes"]:
            node = models.create_node(**n["id"])
            nodes[node.node_id] = node
            nodes_list.append(node)
        data["nodes"] = [{**n, "id": nodes[n["id"]["_node_id"]]} for n in data["nodes"]]
        data["links"] = [
            {**link, "source": nodes[link["source"]], "target": nodes[link["target"]]}
            for link in data["links"]
        ]
        flow.graph = nx.node_link_graph(data)
        return flow

    def __eq__(self, other: "Flow") -> bool:
        return (
            isinstance(other, Flow)
            and self.graph.nodes == other.graph.nodes
            and self.graph.edges == other.graph.edges
        )

    def get_necessary_env_vars(self) -> List[str]:
        env_vars = []
        for node in self.graph.nodes:
            if node.EnvVars:
                env_vars.extend(node.EnvVars.model_fields.keys())
        return env_vars

    def get_issues(self) -> List[str]:
        issues = []
        is_valid = nx.is_directed_acyclic_graph(self.graph)
        if not is_valid:
            issues.append("Graph is not a directed acyclic graph")
        has_trigger = any([node.IS_TRIGGER for node in self.graph.nodes])
        if not has_trigger:
            issues.append("Flow is missing a trigger block")
        if not self.graph.nodes:
            issues.append("Flow is empty")
        # ensure that all nodes are connected (when handle is not optional)
        for node in self.graph.nodes:
            required_inputs = utils.get_required_fields(node.InputSchema)
            for input_name in required_inputs:
                if not any(
                    [
                        (src, tgt, key)
                        for src, tgt, key in self.graph.in_edges(node, data=True)
                        if key["tgt_handle"] == input_name
                    ]
                ):
                    issues.append(
                        f"Node {node.name} is missing required input {input_name}"
                    )

            if node.EnvVars:
                logger.debug(f"Loading env vars for {node}")
                issues.extend(node.EnvVars.get_issues())

        return issues

    def is_valid(self) -> bool:
        return not self.get_issues()

    def get_source_nodes(self) -> List[Node]:
        if not self.is_valid():
            raise ValueError("Cannot get source nodes on invalid flow")
        return [x for x in self.graph.nodes() if self.graph.in_degree(x) == 0]

    def create_template(self):
        template = self.serialize()
        for node in template["nodes"]:
            kls, *_ = models.MAP[node["id"]["kls"]]

            for sensitive_field in kls.SensitiveFields:
                if sensitive_field in node["id"]:
                    del node["id"][sensitive_field]

        return template

    @staticmethod
    def get_overrides_for_template(template) -> Dict[str, BaseModel]:
        required_overrides = {}
        for node in template["nodes"]:
            node_attrs = node["id"]
            name = node_attrs["name"]
            kls, *_ = models.MAP[node_attrs["kls"]]
            init_schema = kls.InitSchema.model_fields

            overrides_for_node = {}
            for field_name, field_info in init_schema.items():
                if field_name in node_attrs:
                    continue
                overrides_for_node[field_name] = (field_info.annotation, field_info)

            schema = create_model(name, **overrides_for_node)
            required_overrides[node_attrs["_node_id"]] = schema

        return required_overrides

    @classmethod
    def from_template(cls, template, data: dict = None):
        data = data or defaultdict(dict)

        flow_json = deepcopy(template)
        for node in flow_json["nodes"]:
            node_id = node["id"]["_node_id"]
            if node_id in data:
                node["id"].update(data[node_id])

        return cls.parse(flow_json)
