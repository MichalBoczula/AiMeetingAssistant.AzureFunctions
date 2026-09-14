import json
import logging

import azure.functions as func

from application.screenshot_request_validator import validate_screenshot_request

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="analyze-screenshot", methods=["POST"])
def analyze_screenshot(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Analyze screenshot request received.")

    request_id = req.form.get("requestId")
    session_id = req.form.get("sessionId")
    screenshot = req.files.get("file")

    error_code = validate_screenshot_request(request_id, session_id, screenshot is not None)

    if error_code is not None:
        return json_response({"errorCode": error_code}, 400)

    return json_response({"requestId": request_id, "status": "accepted"}, 202)


def json_response(payload: dict[str, str], status_code: int) -> func.HttpResponse:
    return func.HttpResponse(json.dumps(payload), status_code=status_code, mimetype="application/json")
