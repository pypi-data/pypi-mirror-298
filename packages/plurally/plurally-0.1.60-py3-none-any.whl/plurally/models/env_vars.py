from pydantic import Field

OpenAiApiKey = Field(
    None,
    title="OpenAI API Key",
    examples=["sk-1234567890abcdef"],
    json_schema_extra={
        "help": "Create an account and find your API key at [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys) to get an API key."
    },
)
