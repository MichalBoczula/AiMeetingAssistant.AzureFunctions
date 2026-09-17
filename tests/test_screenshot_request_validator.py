import pytest

from application.screenshot_request_validator import validate_screenshot_request

PNG = b"\x89PNG\r\n\x1a\ncontent"
JPEG = b"\xff\xd8\xffcontent"
WEBP = b"RIFFxxxxWEBPcontent"


@pytest.mark.parametrize(
    ("request_id", "session_id", "content_type", "content", "expected"),
    [
        (None, "session", "image/png", PNG, "MISSING_REQUEST_ID"),
        ("request", None, "image/png", PNG, "MISSING_SESSION_ID"),
        ("request", "session", None, None, "MISSING_SCREENSHOT"),
        ("request", "session", "application/pdf", PNG, "INVALID_IMAGE_TYPE"),
        ("request", "session", "image/png", PNG * 11, "IMAGE_TOO_LARGE"),
        ("request", "session", "image/png", b"plain text", "INVALID_IMAGE_CONTENT"),
        ("request", "session", "image/png", PNG, None),
        ("request", "session", "image/jpeg", JPEG, None),
        ("request", "session", "image/webp", WEBP, None),
    ],
)
def test_validate_screenshot_request(request_id, session_id, content_type, content, expected):
    assert validate_screenshot_request(request_id, session_id, content_type, content, len(PNG) * 10) == expected
