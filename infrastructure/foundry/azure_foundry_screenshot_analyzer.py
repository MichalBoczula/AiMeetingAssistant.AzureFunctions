import base64
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from openai import OpenAI

DEFAULT_OPENAI_API_VERSION = "2024-10-21"
SCREEN_ANSWER_SYSTEM_PROMPT = (
    "Solve the technical question shown in the screenshot. Read all visible question text, "
    "requirements, diagrams, tables, and answer choices before deciding. Reason silently from "
    "reliable technical knowledge. Never invent facts or guess. If the screenshot is unreadable "
    "or the answer cannot be determined with sufficient confidence, return exactly "
    "'UNSURE: <what information is missing>'. Return only the answer the user can select: for a "
    "multiple-choice question, return the option label and its text; for a Yes/No matrix, return "
    "one line per application in the format '<application>: Yes' or '<application>: No'. Do not "
    "describe the screenshot, restate the question, add an explanation, headings, markdown, or "
    "introductory text."
)


class AzureFoundryScreenshotAnalyzer:
    def __init__(self, client: OpenAI, deployment_name: str):
        self._client = client
        self._deployment_name = deployment_name

    def analyze(self, screenshot_content: bytes, screenshot_content_type: str) -> str:
        response = self._client.chat.completions.create(
            model=self._deployment_name,
            messages=[
                {
                    "role": "system",
                    "content": SCREEN_ANSWER_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Read the complete question and return the selectable answer.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": create_image_data_url(
                                    screenshot_content,
                                    screenshot_content_type,
                                )
                            },
                        },
                    ],
                },
            ],
            max_completion_tokens=500,
        )

        text = response.choices[0].message.content

        if not text:
            raise RuntimeError("Azure Foundry returned an empty analysis.")

        return text


def create_azure_foundry_screenshot_analyzer() -> AzureFoundryScreenshotAnalyzer:
    project_endpoint = get_required_environment_variable("AZURE_AI_PROJECT_ENDPOINT")
    deployment_name = get_required_environment_variable("AZURE_OPENAI_DEPLOYMENT")
    managed_identity_client_id = os.getenv("AZURE_CLIENT_ID")

    project_client = AIProjectClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential(
            managed_identity_client_id=managed_identity_client_id,
        ),
    )

    return AzureFoundryScreenshotAnalyzer(
        project_client.get_openai_client(
            api_version=os.getenv("OPENAI_API_VERSION", DEFAULT_OPENAI_API_VERSION),
        ),
        deployment_name,
    )


def create_image_data_url(screenshot_content: bytes, screenshot_content_type: str) -> str:
    encoded_content = base64.b64encode(screenshot_content).decode("ascii")
    return f"data:{screenshot_content_type};base64,{encoded_content}"


def get_required_environment_variable(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(f"The {name} application setting is required.")

    return value
