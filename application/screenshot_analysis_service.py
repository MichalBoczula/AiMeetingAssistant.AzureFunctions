from application.analysis_completed import AnalysisCompleted
from application.screenshot_analyzer import ScreenshotAnalyzer


class ScreenshotAnalysisService:
    def __init__(self, screenshot_analyzer: ScreenshotAnalyzer):
        self._screenshot_analyzer = screenshot_analyzer

    def analyze(
        self,
        request_id: str,
        session_id: str,
        screenshot_content: bytes,
        screenshot_content_type: str,
    ) -> AnalysisCompleted:
        text = self._screenshot_analyzer.analyze(
            screenshot_content=screenshot_content,
            screenshot_content_type=screenshot_content_type,
        )

        return AnalysisCompleted(
            request_id=request_id,
            session_id=session_id,
            text=text,
        )
