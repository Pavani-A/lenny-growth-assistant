from app.services.growth_assistant_service import GrowthAssistantService


def test_growth_assistant_service():
    service = GrowthAssistantService(
        provider="ollama",
        model="llama3.2:3b",
    )

    answer, sources = service.answer(
        "How can a startup know whether it has product-market fit?",
        top_k=3,
    )

    assert answer
    assert len(sources) == 3

    print("\nANSWER:")
    print(answer)

    print("\nSOURCES:")
    for source in sources:
        print(
            f"- {source['episode_title']} "
            f"({source['guest']})"
        )