def validate_screenshot_request(request_id: str | None, session_id: str | None, has_screenshot: bool) -> str | None:
    if not request_id:
        return "MISSING_REQUEST_ID"
    if not session_id:
        return "MISSING_SESSION_ID"
    if not has_screenshot:
        return "MISSING_SCREENSHOT"
    return None
