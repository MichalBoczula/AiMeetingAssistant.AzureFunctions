SUPPORTED_IMAGE_CONTENT_TYPES = frozenset({"image/jpeg", "image/png", "image/webp"})


def validate_screenshot_request(
    request_id: str | None,
    session_id: str | None,
    screenshot_content_type: str | None,
    screenshot_content: bytes | None,
    max_image_size_bytes: int,
) -> str | None:
    if not request_id:
        return "MISSING_REQUEST_ID"
    if not session_id:
        return "MISSING_SESSION_ID"
    if screenshot_content_type is None or screenshot_content is None:
        return "MISSING_SCREENSHOT"
    if screenshot_content_type not in SUPPORTED_IMAGE_CONTENT_TYPES:
        return "INVALID_IMAGE_TYPE"
    if len(screenshot_content) > max_image_size_bytes:
        return "IMAGE_TOO_LARGE"
    if not has_matching_image_signature(screenshot_content_type, screenshot_content):
        return "INVALID_IMAGE_CONTENT"
    return None


def has_matching_image_signature(content_type: str, content: bytes) -> bool:
    if content_type == "image/png":
        return content.startswith(b"\x89PNG\r\n\x1a\n")
    if content_type == "image/jpeg":
        return content.startswith(b"\xff\xd8\xff")
    if content_type == "image/webp":
        return content.startswith(b"RIFF") and content[8:12] == b"WEBP"
    return False
