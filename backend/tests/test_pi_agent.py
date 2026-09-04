from app.agent.pi_agent import PiAgent


def test_pi_agent_ollama():
    agent = PiAgent(
        provider="ollama",
        model="llama3.2:3b",
    )

    response = agent.generate(
        "Say hello in one short sentence."
    )

    assert response
    print(f"\nPi response: {response}")