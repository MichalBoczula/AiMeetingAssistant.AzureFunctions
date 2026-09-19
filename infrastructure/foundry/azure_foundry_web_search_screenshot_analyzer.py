import base64
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from openai import OpenAI

DEFAULT_OPENAI_API_VERSION = "2024-10-21"
WEB_GROUNDED_SCREENSHOT_PROMPT = (
    "Read the complete technical question in the screenshot, including every requirement, "
    "diagram, table, statement, and answer choice. Use the configured web search tool before "
    "answering to verify the relevant facts. Prefer official vendor documentation. Return only "
    "the selectable answer: for a multiple-choice question, return the option label and text; "
    "for a Yes/No matrix, return one line per item as '<item>: Yes' or '<item>: No'. Do not "
    "describe the screenshot, restate the question, add reasoning, headings, markdown, or "
    "introductory text."
)


class AzureFoundryWebSearchScreenshotAnalyzer:
    def __init__(self, client: OpenAI, agent_name: str):
        self._client = client
        self._agent_name = agent_name

    def analyze(self, screenshot_content: bytes, screenshot_content_type: str) -> str:
        response = self._client.responses.create(
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": WEB_GROUNDED_SCREENSHOT_PROMPT,
                        },
                        {
                            "type": "input_image",
                            "image_url": create_image_data_url(
                                screenshot_content,
                                screenshot_content_type,
                            ),
                            "detail": "high",
                        },
                    ],
                }
            ],
            tool_choice="required",
            extra_body={
                "agent_reference": {
                    "name": self._agent_name,
                    "type": "agent_reference",
                }
            },
        )

        if not response.output_text:
            raise RuntimeError("Foundry web search agent returned an empty analysis.")

        return response.output_text


def create_azure_foundry_web_search_screenshot_analyzer() -> (
    AzureFoundryWebSearchScreenshotAnalyzer
):
    project_endpoint = get_required_environment_variable("AZURE_AI_PROJECT_ENDPOINT")
    agent_name = get_required_environment_variable("AZURE_FOUNDRY_WEB_SEARCH_AGENT_NAME")
    managed_identity_client_id = os.getenv("AZURE_CLIENT_ID")

    project_client = AIProjectClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential(
            managed_identity_client_id=managed_identity_client_id,
        ),
    )

    return AzureFoundryWebSearchScreenshotAnalyzer(
        project_client.get_openai_client(
            api_version=os.getenv("OPENAI_API_VERSION", DEFAULT_OPENAI_API_VERSION),
        ),
        agent_name,
    )


def create_image_data_url(screenshot_content: bytes, screenshot_content_type: str) -> str:
    encoded_content = base64.b64encode(screenshot_content).decode("ascii")
    return f"data:{screenshot_content_type};base64,{encoded_content}"


def get_required_environment_variable(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(f"The {name} application setting is required.")

    return value
