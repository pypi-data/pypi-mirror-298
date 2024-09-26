from sl_ai_models.utils.openai_utils import OpenAiUtils
from tests.ai_mock_manager import AiModelMockManager

################################## Message Creation Tests ##################################
def test_user_message_creator_has_only_one_message():
    messages = OpenAiUtils.put_single_user_message_in_list_using_prompt("Hello")
    length_of_messages = len(messages)
    assert length_of_messages == 1, "Length of user message from propmt is not 1"


def test_system_and_user_message_creator_has_two_messages():
    messages = OpenAiUtils.create_sytem_and_user_message_from_prompt("Hello", "Hi")
    length_of_messages = len(messages)
    assert length_of_messages == 2, "Length of system and user message from propmt is not 2"


def test_vision_message_creator_has_one_message():
    vision_data = AiModelMockManager.CHEAP_IMAGE_MESSAGE_DATA
    messages = OpenAiUtils.put_single_image_message_in_list_using_gpt_vision_input(vision_data)
    length_of_messages = len(messages)
    assert length_of_messages == 1, "Length of vision message from propmt is not 1"


def test_system_and_vision_message_creator_has_two_messages():
    vision_data = AiModelMockManager.CHEAP_IMAGE_MESSAGE_DATA
    messages = OpenAiUtils.create_system_and_image_message_from_prompt(vision_data, "Hi")
    length_of_messages = len(messages)
    assert length_of_messages == 2, "Length of system and vision message from propmt is not 2"