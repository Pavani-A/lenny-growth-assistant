import pytest

from app.retrieval.search import search_transcripts


def test_empty_query_is_rejected():
    with pytest.raises(ValueError, match="Search query cannot be empty"):
        search_transcripts("")


def test_whitespace_query_is_rejected():
    with pytest.raises(ValueError, match="Search query cannot be empty"):
        search_transcripts("   ")


def test_invalid_top_k_is_rejected():
    with pytest.raises(ValueError, match="top_k must be greater than zero"):
        search_transcripts("startup growth", top_k=0)


def test_search_returns_results():
    results = search_transcripts(
        "How should a startup approach growth?",
        top_k=3,
    )

    assert len(results) == 3


def test_search_results_contain_source_information():
    results = search_transcripts(
        "How should a startup approach growth?",
        top_k=1,
    )

    assert len(results) == 1

    result = results[0]

    assert result["episode_id"] is not None
    assert result["episode_title"]
    assert result["content"]
    assert result["distance"] >= 0