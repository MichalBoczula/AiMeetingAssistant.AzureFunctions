from types import SimpleNamespace

import pytest

from infrastructure.foundry.azure_foundry_web_search_screenshot_analyzer import (
    WEB_GROUNDED_SCREENSHOT_PROMPT,
    AzureFoundryWebSearchScreenshotAnalyzer,
    create_image_data_url,
)


class RecordingResponses:
    def __init__(self, output_text: str | None) -> None:
        self._output_text = output_text
        self.kwargs: dict[str, object] | None = None

    def create(self, **kwargs: object) -> object:
        self.kwargs = kwargs
        return SimpleNamespace(output_text=self._output_text)


class FakeAzureOpenAiClient:
    def __init__(self, responses: RecordingResponses) -> None:
        self.responses = responses


def test_analyze_sends_image_to_web_grounded_agent_and_requires_tool_use() -> None:
    responses = RecordingResponses("App1: Yes\nApp2: Yes\nApp3: No\nApp4: Yes")
    analyzer = AzureFoundryWebSearchScreenshotAnalyzer(
        FakeAzureOpenAiClient(responses),
        "az-204-web-search",
    )

    result = analyzer.analyze(b"png-content", "image/png")

    assert result == "App1: Yes\nApp2: Yes\nApp3: No\nApp4: Yes"
    assert responses.kwargs is not None
    assert responses.kwargs["tool_choice"] == "required"
    assert responses.kwargs["extra_body"] == {
        "agent_reference": {
            "name": "az-204-web-search",
            "type": "agent_reference",
        }
    }
    content = responses.kwargs["input"][0]["content"]
    assert content[0]["text"] == WEB_GROUNDED_SCREENSHOT_PROMPT
    assert "Use the configured web search tool before answering" in (
        WEB_GROUNDED_SCREENSHOT_PROMPT
    )
    assert content[1]["image_url"] == "data:image/png;base64,cG5nLWNvbnRlbnQ="
    assert content[1]["detail"] == "high"


def test_analyze_raises_when_agent_returns_empty_text() -> None:
    analyzer = AzureFoundryWebSearchScreenshotAnalyzer(
        FakeAzureOpenAiClient(RecordingResponses(None)),
        "az-204-web-search",
    )

    with pytest.raises(RuntimeError, match="empty analysis"):
        analyzer.analyze(b"png-content", "image/png")


def test_create_image_data_url_encodes_content() -> None:
    assert create_image_data_url(b"hello", "image/webp") == "data:image/webp;base64,aGVsbG8="
