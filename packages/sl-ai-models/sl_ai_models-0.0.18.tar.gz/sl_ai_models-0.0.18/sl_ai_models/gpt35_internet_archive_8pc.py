from typing import Final
from sl_ai_models.model_archetypes.openai_text_model import OpenAiTextToTextModel
from sl_ai_models.utils.ai_misc import clean_indents  # Keep this import here for easier imports into other files so prompts can keep proper indentation levels in code # NOSONAR

class Gpt35InternetArchive8PC(OpenAiTextToTextModel):
    # See OpenAI Limit on the account dashboard for most up-to-date limit
    MODEL_NAME: Final[str] = "ft:gpt-3.5-turbo-0613:internet-archive::8Pco8Os5"
    REQUESTS_PER_PERIOD_LIMIT: Final[int] = 9_000
    REQUEST_PERIOD_IN_SECONDS: Final[int] = 60
    TIMEOUT_TIME: Final[int] = 40
    TOKENS_PER_PERIOD_LIMIT: Final[int] = 8_000_000
    TOKEN_PERIOD_IN_SECONDS: Final[int] = 60
