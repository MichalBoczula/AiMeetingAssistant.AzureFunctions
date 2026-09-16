import json

from application.analysis_completed import AnalysisCompleted
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
