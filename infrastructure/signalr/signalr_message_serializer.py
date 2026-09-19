import json

from application.analysis_completed import AnalysisCompleted
from application.analysis_failed import AnalysisFailed


class SignalRMessageSerializer:
    def serialize(self, analysis_completed: AnalysisCompleted) -> str:
        return json.dumps(
            {
                "target": "AiAnalysisCompleted",
                "arguments": [{"text": analysis_completed.text}],
            }
        )

    def serialize_failed(self, analysis_failed: AnalysisFailed) -> str:
        return json.dumps(
            {
                "target": "AiAnalysisFailed",
                "arguments": [
                    {
                        "requestId": analysis_failed.request_id,
                        "sessionId": analysis_failed.session_id,
                        "status": "failed",
                        "errorCode": analysis_failed.error_code,
                        "message": analysis_failed.message,
                    }
                ],
            }
        )
