from dataclasses import dataclass


@dataclass(frozen=True)
class AnalysisFailed:
    request_id: str
    session_id: str
    error_code: str
    message: str
