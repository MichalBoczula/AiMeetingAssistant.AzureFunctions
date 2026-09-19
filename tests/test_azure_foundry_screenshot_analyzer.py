from types import SimpleNamespace

import pytest

from infrastructure.foundry.azure_foundry_screenshot_analyzer import (
    SCREEN_ANSWER_SYSTEM_PROMPT,
    AzureFoundryScreenshotAnalyzer,
    create_image_data_url,
)


class RecordingCompletions:
    def __init__(self, content: str | None) -> None:
        self._content = content
        self.kwargs: dict[str, object] | None = None

    def create(self, **kwargs: object) -> object:
        self.kwargs = kwargs
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=self._content))]
        )


class FakeAzureOpenAiClient:
    def __init__(self, completions: RecordingCompletions) -> None:
        self.chat = SimpleNamespace(completions=completions)


def test_analyze_sends_complete_question_prompt_and_base64_image_to_foundry() -> None:
    completions = RecordingCompletions(
        "App1: Yes\nApp2: Yes\nApp3: No\nApp4: Yes"
    )
    analyzer = AzureFoundryScreenshotAnalyzer(
        FakeAzureOpenAiClient(completions),
        "gpt-5.4-mini",
    )

    result = analyzer.analyze(b"png-content", "image/png")

    assert result == "App1: Yes\nApp2: Yes\nApp3: No\nApp4: Yes"
    assert completions.kwargs is not None
    assert completions.kwargs["model"] == "gpt-5.4-mini"
    assert completions.kwargs["max_completion_tokens"] == 500
    messages = completions.kwargs["messages"]
    assert messages[0]["content"] == SCREEN_ANSWER_SYSTEM_PROMPT
    assert "Read all visible question text" in SCREEN_ANSWER_SYSTEM_PROMPT
    assert "Never invent facts or guess." in SCREEN_ANSWER_SYSTEM_PROMPT
    assert "Yes/No matrix" in SCREEN_ANSWER_SYSTEM_PROMPT
    assert messages[1]["content"][0]["text"] == (
        "Read the complete question and return the selectable answer."
    )
    assert messages[1]["content"][1]["image_url"]["url"] == (
        "data:image/png;base64,cG5nLWNvbnRlbnQ="
    )


def test_analyze_raises_when_foundry_returns_empty_text() -> None:
    analyzer = AzureFoundryScreenshotAnalyzer(
        FakeAzureOpenAiClient(RecordingCompletions(None)),
        "gpt-5.4-mini",
    )

    with pytest.raises(RuntimeError, match="empty analysis"):
        analyzer.analyze(b"png-content", "image/png")


def test_create_image_data_url_encodes_content() -> None:
    assert create_image_data_url(b"hello", "image/webp") == "data:image/webp;base64,aGVsbG8="
