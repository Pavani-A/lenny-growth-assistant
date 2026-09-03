from pathlib import Path
import subprocess


REPOSITORY_URL = "https://github.com/LennysNewsletter/lennys-newsletterpodcastdata.git"


def clone_repository(destination: Path) -> Path:
    """Clone the official Lenny transcript repository.

    If the repository already exists locally, return its path without
    cloning it again.
    """
    destination = destination.resolve()

    if (destination / ".git").exists():
        return destination

    destination.parent.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            "git",
            "clone",
            REPOSITORY_URL,
            str(destination),
        ],
        check=True,
    )

    return destination