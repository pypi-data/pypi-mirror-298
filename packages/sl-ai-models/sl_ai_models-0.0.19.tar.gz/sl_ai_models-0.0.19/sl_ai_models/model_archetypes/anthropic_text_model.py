from sl_ai_models.utils.response_types import TextTokenCostResponse
from sl_ai_models.model_archetypes.traditional_online_llm import TraditionalOnlineLlm

from langchain_community.callbacks.bedrock_anthropic_callback import _get_anthropic_claude_token_cost, MODEL_COST_PER_1K_INPUT_TOKENS
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate

from abc import ABC
import logging

logger = logging.getLogger(__name__)


class AnthropicTextToTextModel(TraditionalOnlineLlm, ABC):

    def __init__(self, max_tokens: int = 1024, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        assert max_tokens > 0, "Max tokens must be greater than 0"
        self.max_tokens = max_tokens
        self.__anthropic_langchain_llm = ChatAnthropic(
            model_name=self.MODEL_NAME,
            api_key=self.api_key,
            timeout=None,
            stop=None,
            base_url=None,
            max_tokens=self.max_tokens, #type: ignore
            default_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
            max_retries=0 # Retry is implemented locally
        )


    async def invoke(self, prompt: str) -> str:
        response: TextTokenCostResponse =  await self._invoke_with_request_cost_time_and_token_limits_and_retry(prompt)
        return response.data


    async def _mockable_direct_call_to_model(self, prompt: str) -> TextTokenCostResponse:
        self._everything_special_to_call_before_direct_call()
        response: TextTokenCostResponse = await self._call_online_model_using_api(prompt)
        return response


    async def _call_online_model_using_api(self, prompt: str) -> TextTokenCostResponse:
        messages = self._turn_model_input_into_messages(prompt)
        answer_message = await self.__anthropic_langchain_llm.ainvoke(messages)
        answer = answer_message.content

        response_metatdata = answer_message.response_metadata
        prompt_tokens = response_metatdata["usage"]["input_tokens"]
        completion_tokens = response_metatdata["usage"]["output_tokens"]
        total_tokens = prompt_tokens + completion_tokens
        cost = self.caculate_cost_from_tokens(prompt_tkns=prompt_tokens, completion_tkns=completion_tokens)

        assert isinstance(answer, str), "Answer is not a string"
        assert cost >= 0, "Cost is less than 0"
        assert prompt_tokens >= 0, "Prompt Tokens is less than 0"
        assert completion_tokens >= 0, "Completion Tokens is less than 0"

        return TextTokenCostResponse(
            data=answer,
            prompt_tokens_used=prompt_tokens,
            completion_tokens_used=completion_tokens,
            total_tokens_used=total_tokens,
            model=self.MODEL_NAME,
            cost=cost
        )


    def _turn_model_input_into_messages(self, prompt: str) -> list[BaseMessage]:
        if self.system_prompt is None:
            return [HumanMessage(prompt)]
        else:
            chat_template = ChatPromptTemplate.from_messages([
                SystemMessage(content=[
                    {
                        "text": self.system_prompt,
                        "type": "text",
                        "cache_control": {"type": "ephemeral"},
                    }
                ]),
                HumanMessage(prompt)
            ])

            messages = chat_template.invoke({}).to_messages()
            return messages


    ################################## Methods For Mocking/Testing ##################################


    @classmethod
    def _get_mock_return_for_direct_call_to_model_using_cheap_input(cls) -> TextTokenCostResponse:
        cheap_input = cls._get_cheap_input_for_invoke()
        probable_output = "Hello! How can I assist you today? Feel free to ask any questions or let me know if you need help with anything."
        if "opus" in cls.MODEL_NAME.lower():
            probable_output = "Hello! How can I assist you today?"

        model = cls()
        prompt_tokens = model.input_to_tokens(cheap_input)
        completion_tokens = model.__anthropic_langchain_llm.get_num_tokens(probable_output)
        adjustment = 3 # Through manual experimentation, it was found that the number of tokens returned by the API is 3 off for the completion response
        completion_tokens += adjustment
        total_cost = model.caculate_cost_from_tokens(prompt_tkns=prompt_tokens, completion_tkns=completion_tokens)
        total_tokens = prompt_tokens + completion_tokens
        return TextTokenCostResponse (
            data=probable_output,
            prompt_tokens_used=prompt_tokens,
            completion_tokens_used=completion_tokens,
            total_tokens_used=total_tokens,
            model=cls.MODEL_NAME,
            cost=total_cost
        )


    @staticmethod
    def _get_cheap_input_for_invoke() -> str:
        return "Hi"



    ############################# Cost and Token Tracking Methods #############################

    def input_to_tokens(self, prompt: str) -> int:
        messages = self._turn_model_input_into_messages(prompt)
        tokens = self.__anthropic_langchain_llm.get_num_tokens_from_messages(messages)
        adjustment = 0
        for message in messages:
            if isinstance(message, HumanMessage):
                adjustment += 5  # Through manual experimentation, it was found that the number of tokens returned by the API is 5 off for user messages
            if isinstance(message, SystemMessage):
                adjustment -= 31  # Through manual experimentation, it was found that the number of tokens returned by the API is 29 off for system messages. This is not a consisten phenomena for system messages however
        tokens += adjustment
        return tokens


    def caculate_cost_from_tokens(self, prompt_tkns: int, completion_tkns: int) -> float:
        # possible_detailed_model_names = MODEL_COST_PER_1K_INPUT_TOKENS.keys()
        # detailed_model_name = [name for name in possible_detailed_model_names if self.MODEL_NAME in name][0]
        # cost = _get_anthropic_claude_token_cost(prompt_tkns, completion_tkns, detailed_model_name)
        # return cost

        # NOTE: caculate_cost_from_tokens is not implemented since langchain is failing to track the model's cost for models like opus
        return 0



