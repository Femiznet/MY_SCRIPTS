import argparse
from pathlib import Path

def get_directory():
    parser = argparse.ArgumentParser(description="Organize files in a directory.")
    parser.add_argument(
        "dir",
        type=Path,
        help="Path to the directory to organize",
    )

    directory:Path = parser.parse_args().dir

    if not directory.is_dir():
        raise NotADirectoryError(f"Path:{directory.name} is not a directory")

    return directory

if __name__ == "__main__":
    get_directory()