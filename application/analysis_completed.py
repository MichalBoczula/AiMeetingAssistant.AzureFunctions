from dataclasses import dataclass


@dataclass(frozen=True)
class AnalysisCompleted:
    request_id: str
    session_id: str
    text: str
