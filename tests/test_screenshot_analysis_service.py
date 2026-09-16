from application.screenshot_analysis_service import ScreenshotAnalysisService


def test_analyze_returns_temporary_analysis_text() -> None:
    result = ScreenshotAnalysisService().analyze(
        request_id="request-001",
        session_id="session-001",
    )

    assert result.request_id == "request-001"
    assert result.session_id == "session-001"
    assert result.text == "Screenshot received. AI analysis will be added next."
