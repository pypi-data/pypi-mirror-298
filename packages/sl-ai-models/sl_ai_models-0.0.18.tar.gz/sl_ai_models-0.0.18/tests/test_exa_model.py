from unittest.mock import Mock

import pytest

from sl_ai_models.exa_searcher import ExaHighlightQuote, ExaSearcher, ExaSource
from tests.ai_mock_manager import AiModelMockManager


async def test_invoke_for_highlights_in_relevance_order(mocker: Mock) -> None:
    mock_return_value = [
        ExaSource(
            original_query="test query",
            auto_prompt_string=None,
            title="Test Title 1",
            url="https://example1.com",
            text="Test text 1",
            author=None,
            published_date=None,
            score=0.9,
            highlights=["Highlight 1A", "Highlight 1B"],
            highlight_scores=[0.8, 0.6],
        ),
        ExaSource(
            original_query="test query",
            auto_prompt_string=None,
            title="Test Title 2",
            url="https://example2.com",
            text="Test text 2",
            author=None,
            published_date=None,
            score=0.85,
            highlights=["Highlight 2A", "Highlight 2B", "Highlight 2C"],
            highlight_scores=[0.75, 0.7, 0.65],
        ),
    ]
    AiModelMockManager.mock_ai_model_direct_call_with_value(
        mocker, ExaSearcher, mock_return_value
    )

    searcher = ExaSearcher()
    cheap_input = searcher._get_cheap_input_for_invoke()
    result = await searcher.invoke_for_highlights_in_relevance_order(cheap_input)

    assert len(result) == 5
    expected_highlights = [
        ("Highlight 1A", 0.8),
        ("Highlight 2A", 0.75),
        ("Highlight 2B", 0.7),
        ("Highlight 2C", 0.65),
        ("Highlight 1B", 0.6),
    ]

    for i, (expected_highlight, expected_score) in enumerate(expected_highlights):
        assert isinstance(result[i], ExaHighlightQuote)
        assert result[i].highlight_text == expected_highlight
        assert (
            abs(result[i].score - expected_score) < 1e-6
        ), f"Score was {result[i].score}, expected {expected_score}"

    # Check that the highlights are in descending order of score
    for i in range(len(result) - 1):
        assert (
            result[i].score >= result[i + 1].score
        ), f"Highlights not in descending order at index {i}"


@pytest.mark.skip(reason="Not implemented yet. Currently cost more than is worth it")
async def test_with_only_include_highlights() -> None:
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented yet. Currently cost more than is worth it")
async def test_with_only_include_text() -> None:
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented yet. Currently cost more than is worth it")
async def test_with_only_urls() -> None:
    raise NotImplementedError
