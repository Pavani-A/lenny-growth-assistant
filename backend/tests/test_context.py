from app.retrieval.context import build_grounded_context


def test_build_grounded_context():
    context, sources = build_grounded_context(
        "How should a startup find product market fit?",
        top_k=3,
    )

    assert context
    assert len(sources) == 3

    assert "SOURCE 1" in context
    assert "Episode:" in context
    assert "Guest:" in context
    assert "Transcript:" in context