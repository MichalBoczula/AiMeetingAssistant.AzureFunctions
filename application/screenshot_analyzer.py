from typing import Protocol


class ScreenshotAnalyzer(Protocol):
    def analyze(self, screenshot_content: bytes, screenshot_content_type: str) -> str:
        ...
