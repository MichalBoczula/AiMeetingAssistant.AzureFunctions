import pytest

from application.screenshot_request_validator import validate_screenshot_request


@pytest.mark.parametrize(
    ("request_id", "session_id", "content_type", "size", "expected"),
    [
        (None, "session", "image/png", 1, "MISSING_REQUEST_ID"),
        ("request", None, "image/png", 1, "MISSING_SESSION_ID"),
        ("request", "session", None, None, "MISSING_SCREENSHOT"),
        ("request", "session", "application/pdf", 1, "INVALID_IMAGE_TYPE"),
        ("request", "session", "image/png", 11, "IMAGE_TOO_LARGE"),
        ("request", "session", "image/png", 10, None),
        ("request", "session", "image/jpeg", 10, None),
        ("request", "session", "image/webp", 10, None),
    ],
)
def test_validate_screenshot_request(request_id, session_id, content_type, size, expected):
    assert validate_screenshot_request(request_id, session_id, content_type, size, 10) == expected
