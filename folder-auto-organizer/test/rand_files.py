"""Generate random files with random extensions for testing."""

import argparse
import random
import string
from pathlib import Path

EXTENSIONS: list[str] = [
    ".pdf",
    ".docx",
    ".txt",
    ".xlsx",
    ".jpg",
    ".png",
    ".gif",
    ".svg",
    ".zip",
    ".tar",
    ".gz",
    ".py",
    ".js",
    ".html",
    ".css",
    "",
]


def _generate_random_file(path:Path, dir:bool) -> None:
    """Generate a random filename with a random extension."""
    name_length = random.randint(5, 12)
    name = "".join(random.choices(string.ascii_lowercase, k=name_length))
    if not dir:
        ext = random.choice(EXTENSIONS)
        file = path / f"{name}{ext}"
        return file.touch()
    
    return (path / name).mkdir(exist_ok=True)


def _generate_files(count: int, output_dir: Path) -> None:
    """Create specified number of random files in the output directory."""
    output_dir.mkdir(parents=True, exist_ok=True)

    for i in range(count):
        choice = i % 2 == 0
        _generate_random_file(output_dir, dir=choice)


def create_random_files(dirname:str, count:int) -> None:
    
    """Parse arguments and run file generator."""
    parser = argparse.ArgumentParser(
        description="Generate random files for testing."
    )
    parser.add_argument(
        "count",
        type=int,
        default=count,
        help="Number of random files to generate",
    )
    parser.add_argument(
        "--dir",
        type=str,
        default=dirname,
        help="Target directory to create files in",
    )

    args = parser.parse_args()

    _generate_files(args.count, Path(args.dir))


if __name__ == "__main__":
    dirname = "test_files"
    count = 1000

    create_random_files(dirname, count)