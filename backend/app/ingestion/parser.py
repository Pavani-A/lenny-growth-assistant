import json
from datetime import date
from pathlib import Path


def load_index(repository_path: Path) -> list[dict]:
    """Load podcast metadata from the repository index.json."""
    index_path = repository_path / "index.json"

    if not index_path.exists():
        raise FileNotFoundError(
            f"Could not find transcript index: {index_path}"
        )

    with index_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Expected index.json to contain an object.")

    podcasts = data.get("podcasts")

    if not isinstance(podcasts, list):
        raise ValueError(
            "Expected index.json to contain a 'podcasts' list."
        )

    return podcasts


def parse_date(value: str | None) -> date | None:
    """Convert an ISO date string into a Python date."""
    if not value:
        return None

    return date.fromisoformat(value)


def parse_podcast_metadata(item: dict) -> dict:
    """Convert one podcast entry into application metadata."""
    return {
        "title": item["title"],
        "guest": item.get("guest"),
        "description": item.get("description"),
        "published_date": parse_date(item.get("date")),
        "source_url": item.get("post_url"),
        "youtube_url": item.get("youtube_url"),
        "filename": item["filename"],
        "word_count": item.get("word_count"),
    }
def load_transcript_content(
    repository_path: Path,
    filename: str,
) -> str:
    """Load transcript text from a Markdown file.

    The repository stores metadata in YAML-style front matter at the
    beginning of each transcript. This function removes that front
    matter and returns only the transcript content.
    """
    transcript_path = repository_path / filename

    if not transcript_path.exists():
        raise FileNotFoundError(
            f"Could not find transcript: {transcript_path}"
        )

    text = transcript_path.read_text(encoding="utf-8")

    if text.startswith("---"):
        parts = text.split("---", 2)

        if len(parts) == 3:
            text = parts[2]

    return text.strip()