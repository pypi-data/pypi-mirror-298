from __future__ import annotations

from sl_ai_models.utils.jsonable import Jsonable
from sl_ai_models.basic_model_interfaces.request_limited_model import RequestLimitedModel
from sl_ai_models.basic_model_interfaces.retryable_model import RetryableModel
from sl_ai_models.basic_model_interfaces.time_limited_model import TimeLimitedModel
from sl_ai_models.basic_model_interfaces.priced_per_request import PricedPerRequest
from sl_ai_models.basic_model_interfaces.incurs_cost import IncursCost
from sl_ai_models.resource_managers.monetary_cost_manager import MonetaryCostManager

from pydantic import BaseModel
import os
import aiohttp
import logging
logger = logging.getLogger(__name__)

class ExaSource(BaseModel, Jsonable):
    original_query: str
    auto_prompt_string: str | None
    title: str | None
    url: str | None
    text: str | None
    author: str | None
    published_date: str | None
    score: float | None
    highlights: list[str]
    highlight_scores: list[float]


class ExaHighlightQuote(BaseModel, Jsonable):
    highlight_text: str
    score: float
    source: ExaSource


class ExaSearcher(RequestLimitedModel, RetryableModel, TimeLimitedModel, IncursCost):
    REQUESTS_PER_PERIOD_LIMIT = 25  # 25 is a guess from manual experimentation since they don't seem to publish this in an obvious place
    REQUEST_PERIOD_IN_SECONDS = 60
    TIMEOUT_TIME = 30
    COST_PER_REQUEST = 0.005
    COST_PER_HIGHLIGHT = 0.0001
    COST_PER_TEXT = 0.0001

    def __init__(
        self,
        *args,
        include_text: bool = False,
        include_highlights: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.include_text = include_text
        self.include_highlights = include_highlights
        self.num_highlights_per_url = 10
        self.num_sentences_per_highlight = 4
        self.num_results = 20

    async def invoke_for_highlights_in_relevance_order(
        self, search_query: str
    ) -> list[ExaHighlightQuote]:
        assert (
            self.include_highlights
        ), "include_highlights must be true to use this method"
        sources = await self.invoke(search_query)
        all_highlights = []
        for source in sources:
            for highlight, score in zip(source.highlights, source.highlight_scores):
                all_highlights.append(
                    ExaHighlightQuote(
                        highlight_text=highlight, score=score, source=source
                    )
                )
        sorted_highlights = sorted(all_highlights, key=lambda x: x.score, reverse=True)
        return sorted_highlights

    async def invoke(self, search_query: str) -> list[ExaSource]:
        return await self.__retryable_timed_cost_request_limited_invoke(search_query)

    @RetryableModel._retry_according_to_model_allowed_tries
    @RequestLimitedModel._wait_till_request_capacity_available
    @IncursCost._wrap_in_cost_limiting_and_tracking
    @TimeLimitedModel._wrap_in_model_defined_timeout
    async def __retryable_timed_cost_request_limited_invoke(
        self, search_query: str
    ) -> list[ExaSource]:
        if not search_query:
            raise ValueError("search_query is required")
        response = await self._mockable_direct_call_to_model(search_query)
        return response

    async def _mockable_direct_call_to_model(
        self, search_query: str
    ) -> list[ExaSource]:
        self._everything_special_to_call_before_direct_call()
        api_key = self._get_api_key()
        url, headers, payload = self._prepare_request_data(api_key, search_query)
        response_data = await self._make_api_request(url, headers, payload)
        exa_sources = self._process_response(response_data, search_query)
        self._log_results(exa_sources)
        return exa_sources

    def _get_api_key(self) -> str:
        api_key = os.getenv("EXA_API_KEY")
        assert api_key is not None, "EXA_API_KEY is not set in the environment variables"
        return api_key

    def _prepare_request_data(self, api_key: str, search_query: str) -> tuple[str, dict, dict]:
        url = "https://api.exa.ai/search"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": api_key,
        }
        text_mode = {"includeHtmlTags": False} if self.include_text else False
        highlights_mode = (
            {
                "numSentences": self.num_sentences_per_highlight,
                "highlightsPerUrl": self.num_highlights_per_url,
                "query": search_query,
            }
            if self.include_highlights
            else False
        )
        payload = {
            "query": search_query,
            "type": "neural",
            "useAutoprompt": True,
            "numResults": self.num_results,
            "contents": {
                "text": text_mode,
                "highlights": highlights_mode,
            },
        }
        return url, headers, payload

    async def _make_api_request(self, url: str, headers: dict, payload: dict) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                response.raise_for_status()
                result: dict = await response.json()
                return result

    def _process_response(self, response_data: dict, search_query: str) -> list[ExaSource]:
        exa_sources: list[ExaSource] = []
        auto_prompt_string = response_data.get("autopromptString")
        for result in response_data["results"]:
            assert isinstance(result, dict), "result is not a dict"
            exa_source = ExaSource(
                original_query=search_query,
                auto_prompt_string=auto_prompt_string,
                title=result.get("title"),
                url=result.get("url"),
                text=result.get("text"),
                author=result.get("author"),
                published_date=result.get("publishedDate"),
                score=result.get("score"),
                highlights=result.get("highlights", []),
                highlight_scores=result.get("highlightScores", []),
            )
            exa_sources.append(exa_source)
        return exa_sources

    def _log_results(self, exa_sources: list[ExaSource]) -> None:
        logger.debug(
            f"Exa API returned {len(exa_sources)} sources with urls: {[source.url for source in exa_sources]}"
        )

    ##################################### Cost Calculation #####################################

    def _caculate_cost_for_request(self, results: list[ExaSource]) -> float:
        cost = self.COST_PER_REQUEST
        cost += self.COST_PER_TEXT * len(results) if self.include_text else 0
        cost += self.COST_PER_HIGHLIGHT * len(results) if self.include_highlights else 0
        return cost

    def _estimate_final_of_running_model_input(self, input_to_model: str) -> float:
        estimated_num_results = self.num_results
        mock_exa_source = self._get_mock_return_for_direct_call_to_model_using_cheap_input()[0]
        cost = self._caculate_cost_for_request([mock_exa_source] * estimated_num_results)
        return cost

    async def _track_cost_in_manager_using_model_response(
        self,
        response_from_direct_call: list[ExaSource],
    ) -> None:
        assert isinstance(
            response_from_direct_call, list
        ), f"response_from_direct_call is not a list, it is a {type(response_from_direct_call)}"
        cost = self._caculate_cost_for_request(response_from_direct_call)
        MonetaryCostManager.increase_current_usage_in_parent_managers(cost)


    ################################### Mocking/Test Functions ###################################
    @staticmethod
    def _get_mock_return_for_direct_call_to_model_using_cheap_input() -> (
        list[ExaSource]
    ):
        return [
            ExaSource(
                original_query="Moko Research Website",
                auto_prompt_string="Here is a link to the Moko Research website:",
                title="MokoResearch",
                url="https://www.mokoresearch.com",
                text="Fake text",
                author=None,
                published_date=None,
                score=0.99,
                highlights=["Fake highlight 1", "Fake highlight 2"],
                highlight_scores=[0.5, 0.6],
            )
        ]

    @staticmethod
    def _get_cheap_input_for_invoke() -> str:
        return "Moko Research Website"