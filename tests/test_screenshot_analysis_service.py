from application.screenshot_analysis_service import ScreenshotAnalysisService


class FakeScreenshotAnalyzer:
    def __init__(self) -> None:
        self.screenshot_content: bytes | None = None
        self.screenshot_content_type: str | None = None

    def analyze(self, screenshot_content: bytes, screenshot_content_type: str) -> str:
        self.screenshot_content = screenshot_content
        self.screenshot_content_type = screenshot_content_type
        return "Explain the highlighted release risk."


def test_analyze_delegates_screenshot_to_analyzer_and_returns_completed_analysis() -> None:
    analyzer = FakeScreenshotAnalyzer()
    service = ScreenshotAnalysisService(analyzer)

    result = service.analyze(
        request_id="request-001",
        session_id="session-001",
        screenshot_content=b"image-content",
        screenshot_content_type="image/png",
    )

    assert analyzer.screenshot_content == b"image-content"
    assert analyzer.screenshot_content_type == "image/png"
    assert result.request_id == "request-001"
    assert result.session_id == "session-001"
    assert result.text == "Explain the highlighted release risk."
