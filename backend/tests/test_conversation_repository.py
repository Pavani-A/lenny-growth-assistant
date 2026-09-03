import uuid

import pytest

from app.db.database import SessionLocal
from app.repositories.conversation_repository import ConversationRepository


@pytest.fixture
def db():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def repository():
    return ConversationRepository()


def test_create_conversation(db, repository):
    session_id = f"test-session-{uuid.uuid4()}"

    conversation = repository.get_or_create_conversation(
        db=db,
        session_id=session_id,
        user_id="test-user",
    )

    assert conversation.id is not None
    assert conversation.session_id == session_id
    assert conversation.user_id == "test-user"


def test_get_or_create_reuses_existing_conversation(db, repository):
    session_id = f"test-session-{uuid.uuid4()}"

    first = repository.get_or_create_conversation(
        db=db,
        session_id=session_id,
        user_id="test-user",
    )

    second = repository.get_or_create_conversation(
        db=db,
        session_id=session_id,
        user_id="test-user",
    )

    assert first.id == second.id
    assert second.session_id == session_id


def test_add_and_get_messages(db, repository):
    session_id = f"test-session-{uuid.uuid4()}"

    conversation = repository.get_or_create_conversation(
        db=db,
        session_id=session_id,
        user_id="test-user",
    )

    user_message = repository.add_message(
        db=db,
        conversation_id=conversation.id,
        role="user",
        content="What is product-market fit?",
    )

    assistant_message = repository.add_message(
        db=db,
        conversation_id=conversation.id,
        role="assistant",
        content="Product-market fit means customers consistently value the product.",
    )

    messages = repository.get_messages(
        db=db,
        conversation_id=conversation.id,
    )

    assert len(messages) == 2

    assert messages[0].id == user_message.id
    assert messages[0].role == "user"
    assert messages[0].content == "What is product-market fit?"

    assert messages[1].id == assistant_message.id
    assert messages[1].role == "assistant"
    assert messages[1].content.startswith("Product-market fit")


def test_invalid_role_is_rejected(db, repository):
    session_id = f"test-session-{uuid.uuid4()}"

    conversation = repository.get_or_create_conversation(
        db=db,
        session_id=session_id,
        user_id="test-user",
    )

    with pytest.raises(
        ValueError,
        match="Message role must be either 'user' or 'assistant'",
    ):
        repository.add_message(
            db=db,
            conversation_id=conversation.id,
            role="system",
            content="Invalid message",
        )


def test_empty_message_is_rejected(db, repository):
    session_id = f"test-session-{uuid.uuid4()}"

    conversation = repository.get_or_create_conversation(
        db=db,
        session_id=session_id,
        user_id="test-user",
    )

    with pytest.raises(
        ValueError,
        match="Message content cannot be empty",
    ):
        repository.add_message(
            db=db,
            conversation_id=conversation.id,
            role="user",
            content="   ",
        )
def test_existing_conversation_updates_user_id(db, repository):
    session_id = f"test-session-{uuid.uuid4()}"

    conversation = repository.get_or_create_conversation(
        db=db,
        session_id=session_id,
    )

    assert conversation.user_id is None

    updated_conversation = repository.get_or_create_conversation(
        db=db,
        session_id=session_id,
        user_id="test-user",
    )

    assert updated_conversation.id == conversation.id
    assert updated_conversation.user_id == "test-user"