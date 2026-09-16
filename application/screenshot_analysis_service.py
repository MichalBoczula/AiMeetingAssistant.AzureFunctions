from application.analysis_completed import AnalysisCompleted


class ScreenshotAnalysisService:
    def analyze(self, request_id: str, session_id: str) -> AnalysisCompleted:
        return AnalysisCompleted(
            request_id=request_id,
            session_id=session_id,
            text="Screenshot received. AI analysis will be added next.",
        )
