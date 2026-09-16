import json

from application.analysis_completed import AnalysisCompleted


class SignalRMessageSerializer:
    def serialize(self, analysis_completed: AnalysisCompleted) -> str:
        return json.dumps(
            {
                "target": "AiAnalysisCompleted",
                "arguments": [{"text": analysis_completed.text}],
            }
        )
