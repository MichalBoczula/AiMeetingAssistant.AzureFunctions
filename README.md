# AiMeetingAssistant.AzureFunctions
Python Azure Functions for AI Meeting Assistant.

## Question analysis

The active Foundry web search adapter accepts both direct screenshots and camera
photographs. Its request prompt focuses on the complete question and related
choices, code, diagrams, and tables, while ignoring unrelated interface elements
and physical surroundings. It verifies technical facts through the configured web
search tool and returns only the answer in plain text. Choices without visible
labels are returned as answer text, without invented letters or numbers.

If essential content is missing or unreadable, or the evidence does not support an
answer, the agent is instructed to return a short `Cannot determine: ...` message.
This prompt does not crop, sharpen, or reconstruct the image and does not guarantee
answer accuracy. Keep the complete question and all options readable in the frame.

The request prompt is defined as `WEB_GROUNDED_SCREENSHOT_PROMPT` in
`infrastructure/foundry/azure_foundry_web_search_screenshot_analyzer.py`. Deploy the
Function after merging changes to activate it. Instructions saved separately on
the Foundry agent should be consistent with this question-focused behavior.
