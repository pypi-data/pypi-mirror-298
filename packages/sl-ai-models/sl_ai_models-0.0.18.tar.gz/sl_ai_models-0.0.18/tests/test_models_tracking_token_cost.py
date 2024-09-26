import pytest
from tests.models_to_test import ModelsToTest
import asyncio
from sl_ai_models.basic_model_interfaces.priced_per_request import PricedPerRequest
from sl_ai_models.basic_model_interfaces.tokens_incur_cost import TokensIncurCost
from sl_ai_models.utils.response_types import TextTokenCostResponse
from sl_ai_models.basic_model_interfaces.ai_model import AiModel
from sl_ai_models.model_archetypes.traditional_online_llm import TraditionalOnlineLlm

@pytest.mark.parametrize(
    "subclass",
    ModelsToTest.TOKENS_INCUR_COST_LIST
)
def test_predicted_cost_and_tokens_correct_for_cheap_input(subclass: type[TokensIncurCost]) -> None:
    model = subclass()
    assert_cost_and_tokens_correct_for_cheap_input(model)


@pytest.mark.parametrize(
    "subclass",
    ModelsToTest.TOKENS_INCUR_COST_LIST
)
def test_system_prompt_cost_and_tokens_correct_for_cheap_input(subclass: type[TokensIncurCost]) -> None:
    if not issubclass(subclass, TraditionalOnlineLlm):
        pytest.skip("Model doesn't have a system prompt")

    model_without_system_prompt = subclass()
    model_with_system_prompt = subclass(system_prompt="this is a system prompt")
    cheap_input = model_without_system_prompt._get_cheap_input_for_invoke()

    with_system_prompt_tokens = model_with_system_prompt.input_to_tokens(cheap_input)
    model_without_system_prompt_tokens = model_without_system_prompt.input_to_tokens(cheap_input)
    assert with_system_prompt_tokens != model_without_system_prompt_tokens, "Token cost should differ if system prompt is set"

    assert_cost_and_tokens_correct_for_cheap_input(model_with_system_prompt)



def assert_cost_and_tokens_correct_for_cheap_input(model: TokensIncurCost) -> None:
    assert isinstance(model, AiModel), "model must be an instance of AiModel"

    cheap_input = model._get_cheap_input_for_invoke()

    predicted_prompt_tokens = model.input_to_tokens(cheap_input)
    predicted_prompt_cost_v1 = model.caculate_cost_from_tokens(predicted_prompt_tokens,0)
    predicted_prompt_cost_v2 = model.cost_per_token_prompt * predicted_prompt_tokens

    response = asyncio.run(model._mockable_direct_call_to_model(cheap_input))

    if not isinstance(response, TextTokenCostResponse):
        raise ValueError("response must be a TextTokenCostResponse or the test will fail")

    actual_prompt_tokens = response.prompt_tokens_used
    actual_completion_tokens = response.completion_tokens_used
    actual_cost = response.cost

    predicted_completion_cost_v1 = model.caculate_cost_from_tokens(0,actual_completion_tokens)
    if isinstance(model, PricedPerRequest):
        predicted_completion_cost_v1 -= model.PRICE_PER_REQUEST
    predicted_completion_cost_v2 = model.cost_per_token_completion * actual_completion_tokens

    predicted_total_cost_v1 = predicted_prompt_cost_v1 + predicted_completion_cost_v1
    predicted_total_cost_v2 = predicted_prompt_cost_v2 + predicted_completion_cost_v2

    allowed_error = 0.0001
    assert predicted_prompt_tokens == actual_prompt_tokens, f"predicted tokens different than actual tokens. Predicted: {predicted_prompt_tokens}, Actual: {actual_prompt_tokens}"
    assert abs(predicted_total_cost_v1 - actual_cost) < allowed_error, f"predicted cost different than actual cost using method 1. Predicted: {predicted_prompt_cost_v1}, Actual: {actual_cost}"

    predicted_cost_v2_within_allowed_error = abs(predicted_total_cost_v2 - actual_cost) < allowed_error
    if not isinstance(model, PricedPerRequest):
        assert predicted_cost_v2_within_allowed_error, f"predicted cost different than actual cost using method 2. Predicted: {predicted_prompt_cost_v2}, Actual: {actual_cost}"
    else:
        assert not predicted_cost_v2_within_allowed_error, "Price per request should have broken this"