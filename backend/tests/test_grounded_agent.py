from app.agent.grounded_agent import GroundedLennyAgent


def test_grounded_lenny_agent():
    agent = GroundedLennyAgent(
        provider="ollama",
        model="llama3.2:3b",
    )

    result = agent.answer(
        "How can a startup know whether it has product-market fit?",
        top_k=3,
    )

    assert result.answer
    assert len(result.sources) == 3

    print("\nANSWER:")
    print(result.answer)

    print("\nSOURCES:")
    for source in result.sources:
        print(
            f"- {source['episode_title']} "
            f"({source['guest']})"
        )