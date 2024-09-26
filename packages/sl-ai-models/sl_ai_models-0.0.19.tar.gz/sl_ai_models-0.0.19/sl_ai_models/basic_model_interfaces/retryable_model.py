from __future__ import annotations
from abc import ABC
from typing import Any
from sl_ai_models.basic_model_interfaces.ai_model import AiModel
from typing import Callable, TypeVar, Coroutine
import logging
logger = logging.getLogger(__name__)
import functools
from tenacity import retry, wait_random_exponential, stop_after_attempt


T = TypeVar('T')



class RetryableModel(AiModel, ABC):
    _DEFAULT_ALLOWED_TRIES: int = 3

    def __init__(self, allowed_tries: int = _DEFAULT_ALLOWED_TRIES, **kwargs) -> None:
        super().__init__(**kwargs)
        if isinstance(allowed_tries, int) and allowed_tries > 0:
            self.allowed_tries = allowed_tries
        else:
            raise ValueError(f"allowed_tries must exist and be an integer greater than 0. allowed_tries was: {allowed_tries}")


    @property
    def allowed_tries(self) -> int:
        return self.__allowed_tries


    @allowed_tries.setter
    def allowed_tries(self, value: int) -> None:
        if not isinstance(value, int) or value < 1:
            raise ValueError("allowed_tries must be an integer greater than 0.")
        self.__allowed_tries = value


    @staticmethod
    def _retry_according_to_model_allowed_tries(func: Callable[..., Coroutine[Any, Any, T]]) -> Callable[..., Coroutine[Any, Any, T]]:
        @functools.wraps(func)
        async def wrapper_with_access_to_self_variable(self: RetryableModel, *args, **kwargs) -> T:
            @retry(
                wait=wait_random_exponential(exp_base=2, multiplier=10, min=5, max=60), # Waits random number between 0 and exp_base^current_attempt * multiplier (with min and max override as needed)
                reraise=True,
                stop=stop_after_attempt(self.allowed_tries)
            )
            async def wrapper_with_action(self: RetryableModel, *args, **kwargs) -> T:
                result = await func(self, *args, **kwargs)
                return result
            return await wrapper_with_action(self, *args, **kwargs)
        return wrapper_with_access_to_self_variable

