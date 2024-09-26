from typing import Final
from sl_ai_models.model_archetypes.openai_vision_model import OpenAiVisionToTextModel
from sl_ai_models.utils.openai_utils import VisionMessageData
from sl_ai_models.utils.ai_misc import clean_indents  # Keep this import here for easier imports into other files so prompts can keep proper indentation levels in code # NOSONAR

class Gpt4VisionInput(VisionMessageData):
    # This class is just to allow additional fields later, and easier imports so you can import all you need from one file
    pass


class Gpt4oVision(OpenAiVisionToTextModel):
    # See OpenAI Limit on the account dashboard for most up-to-date limit
    MODEL_NAME: Final[str] = "gpt-4o"
    REQUESTS_PER_PERIOD_LIMIT: Final[int] = 9_000
    REQUEST_PERIOD_IN_SECONDS: Final[int] = 60
    TIMEOUT_TIME: Final[int] = 40
    TOKENS_PER_PERIOD_LIMIT: Final[int] = 8_000_000
    TOKEN_PERIOD_IN_SECONDS: Final[int] = 60


