import json
import logging
import os
from functools import lru_cache

import azure.functions as func

from application.screenshot_analysis_service import ScreenshotAnalysisService
from application.screenshot_request_validator import validate_screenshot_request
from infrastructure.foundry.azure_foundry_web_search_screenshot_analyzer import (
    create_azure_foundry_web_search_screenshot_analyzer,
)
from infrastructure.signalr.signalr_message_serializer import SignalRMessageSerializer

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

signalr_message_serializer = SignalRMessageSerializer()


@app.generic_output_binding(
    arg_name="signalr_messages",
    type="signalR",
    hubName="meeting",
    connectionStringSetting="AzureSignalRConnectionString",
)
@app.route(route="analyze-screenshot", methods=["POST"])
def analyze_screenshot(
    req: func.HttpRequest, signalr_messages: func.Out[str]
) -> func.HttpResponse:
    logging.info("Analyze screenshot request received.")

    request_id = req.form.get("requestId")
    session_id = req.form.get("sessionId")
    screenshot = req.files.get("file")
    screenshot_content = screenshot.read() if screenshot else None
    screenshot_content_type = screenshot.content_type if screenshot else None

    error_code = validate_screenshot_request(
        request_id=request_id,
        session_id=session_id,
        screenshot_content_type=screenshot_content_type,
        screenshot_content=screenshot_content,
        max_image_size_bytes=get_max_image_size_bytes(),
    )

    if error_code is not None:
        return json_response({"errorCode": error_code}, 400)

    try:
        analysis_completed = get_analysis_service().analyze(
            request_id=request_id,
            session_id=session_id,
            screenshot_content=screenshot_content,
            screenshot_content_type=screenshot_content_type,
        )
    except Exception:
        logging.exception("Screenshot analysis failed.")
        return json_response({"errorCode": "ANALYSIS_UNAVAILABLE"}, 502)

    signalr_messages.set(signalr_message_serializer.serialize(analysis_completed))

    return json_response({"requestId": request_id, "status": "accepted"}, 202)


@app.generic_input_binding(
    arg_name="connection_info",
    type="signalRConnectionInfo",
    hubName="meeting",
    connectionStringSetting="AzureSignalRConnectionString",
)
@app.route(route="negotiate", methods=["POST"])
def negotiate(req: func.HttpRequest, connection_info: str) -> func.HttpResponse:
    return func.HttpResponse(connection_info, status_code=200, mimetype="application/json")


@lru_cache
def get_analysis_service() -> ScreenshotAnalysisService:
    return ScreenshotAnalysisService(
        create_azure_foundry_web_search_screenshot_analyzer()
    )


def get_max_image_size_bytes() -> int:
    return int(os.getenv("AI_MAX_IMAGE_SIZE_MB", "10")) * 1024 * 1024


def json_response(payload: dict[str, str], status_code: int) -> func.HttpResponse:
    return func.HttpResponse(json.dumps(payload), status_code=status_code, mimetype="application/json")
