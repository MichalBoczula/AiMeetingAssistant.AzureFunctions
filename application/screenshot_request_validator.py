SUPPORTED_IMAGE_CONTENT_TYPES = frozenset({"image/jpeg", "image/png", "image/webp"})


def validate_screenshot_request(
    request_id: str | None,
    session_id: str | None,
    screenshot_content_type: str | None,
    screenshot_size_bytes: int | None,
    max_image_size_bytes: int,
) -> str | None:
    if not request_id:
        return "MISSING_REQUEST_ID"
    if not session_id:
        return "MISSING_SESSION_ID"
    if screenshot_content_type is None or screenshot_size_bytes is None:
        return "MISSING_SCREENSHOT"
    if screenshot_content_type not in SUPPORTED_IMAGE_CONTENT_TYPES:
        return "INVALID_IMAGE_TYPE"
    if screenshot_size_bytes > max_image_size_bytes:
        return "IMAGE_TOO_LARGE"
    return None
