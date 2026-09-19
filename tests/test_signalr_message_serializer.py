import json

from application.analysis_completed import AnalysisCompleted
from application.analysis_failed import AnalysisFailed
from infrastructure.signalr.signalr_message_serializer import SignalRMessageSerializer


def test_serialize_creates_ai_analysis_completed_signalr_message() -> None:
    analysis_completed = AnalysisCompleted(
        request_id="request-001",
        session_id="session-001",
        text="Discuss the release timeline.",
    )

    message = json.loads(SignalRMessageSerializer().serialize(analysis_completed))

    assert message == {
        "target": "AiAnalysisCompleted",
        "arguments": [{"text": "Discuss the release timeline."}],
    }


def test_serialize_failed_creates_ai_analysis_failed_signalr_message() -> None:
    analysis_failed = AnalysisFailed(
        request_id="request-001",
        session_id="session-001",
        error_code="RATE_LIMITED",
        message="AI is temporarily busy. Please try again in about a minute.",
    )

    message = json.loads(SignalRMessageSerializer().serialize_failed(analysis_failed))

    assert message == {
        "target": "AiAnalysisFailed",
        "arguments": [
            {
                "requestId": "request-001",
                "sessionId": "session-001",
                "status": "failed",
                "errorCode": "RATE_LIMITED",
                "message": "AI is temporarily busy. Please try again in about a minute.",
            }
        ],
    }
