import pytest
from application.screenshot_request_validator import validate_screenshot_request


@pytest.mark.parametrize(
    ("request_id", "session_id", "has_screenshot", "expected"),
    [
        (None, "session", True, "MISSING_REQUEST_ID"),
        ("request", None, True, "MISSING_SESSION_ID"),
        ("request", "session", False, "MISSING_SCREENSHOT"),
        ("request", "session", True, None),
    ],
)
def test_validate_screenshot_request(request_id, session_id, has_screenshot, expected):
    assert validate_screenshot_request(request_id, session_id, has_screenshot) == expected
