from pathlib import Path

from app.ingestion.chunker import chunk_text
from app.ingestion.parser import (
    load_index,
    load_transcript_content,
    parse_podcast_metadata,
)


REPOSITORY_PATH = Path(__file__).resolve().parents[2] / "data" / "lenny-transcripts"


def test_load_index():
    items = load_index(REPOSITORY_PATH)

    assert len(items) > 0
    assert "title" in items[0]
    assert "filename" in items[0]


def test_parse_podcast_metadata():
    items = load_index(REPOSITORY_PATH)
    metadata = parse_podcast_metadata(items[0])

    assert metadata["title"]
    assert metadata["filename"]
    assert metadata["published_date"] is not None


def test_load_transcript_content():
    items = load_index(REPOSITORY_PATH)

    content = load_transcript_content(
        REPOSITORY_PATH,
        items[0]["filename"],
    )

    assert content
    assert not content.startswith("---")


def test_chunk_text():
    text = "one two three four five six seven eight nine ten"

    chunks = chunk_text(
        text,
        chunk_size=5,
        overlap=2,
    )

    assert chunks == [
        "one two three four five",
        "four five six seven eight",
        "seven eight nine ten",
    ]