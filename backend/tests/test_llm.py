import pytest

from app.llm.ollama import OllamaProvider


def test_ollama_provider_generates_response():
    provider = OllamaProvider()

    response = provider.generate(
        "Explain product growth in one sentence."
    )

    assert response
    assert isinstance(response, str)


def test_ollama_provider_rejects_empty_prompt():
    provider = OllamaProvider()

    with pytest.raises(ValueError, match="Prompt cannot be empty"):
        provider.generate("")


def test_ollama_provider_supports_system_prompt():
    provider = OllamaProvider()

    response = provider.generate(
        "What is 2 + 2?",
        system_prompt="Answer using only one short sentence.",
    )

    assert response
    assert isinstance(response, str)