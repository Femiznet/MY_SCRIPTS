"""
lookup.py - Search a directory tree for files or folders by pattern,
then optionally open or delete what you find.

Usage examples:
    python lookup.py --path ./src --pattern "*.py"
    python lookup.py --path ./src --pattern "*.py" --action open --onfirst
    python lookup.py --path ./logs --pattern "*.log" --action delete
    python lookup.py --path ./src --pattern "tests" --dir
"""

__version__ = "1.0.0"

import argparse
import fnmatch
import os
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------

class Action(str, Enum):
    OPEN   = "open"
    DELETE = "delete"


class TargetKind(str, Enum):
    FILE      = "file"
    DIRECTORY = "directory"


@dataclass(frozen=True)
class SearchConfig:
    """Everything the program needs to know, validated up-front."""
    root:     Path
    pattern:  str
    action:   Action | None
    onfirst:  bool
    kind:     TargetKind


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def parse_args_legacy() -> SearchConfig:
    """Parse traditional --flag arguments (internal use)."""
    parser = argparse.ArgumentParser(
        description="Lookup files or directories by pattern, then open or delete them.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--path",
        required=True,
        metavar="DIR",
        help="Root directory to start searching from.",
    )
    parser.add_argument(
        "--pattern",
        required=True,
        metavar="GLOB",
        help='Glob pattern to match names against, e.g. "*.py" or "test_*".',
    )
    parser.add_argument(
        "--action",
        choices=[a.value for a in Action],
        default=None,
        help="What to do with a match: open it in the default app, or delete it.",
    )
    parser.add_argument(
        "--onfirst",
        action="store_true",
        help="Apply the action to the very first match found, then stop.",
    )
    parser.add_argument(
        "--dir",
        action="store_true",
        help="Search for directories instead of files.",
    )

    args = parser.parse_args()

    root = Path(args.path)
    if not root.is_dir():
        parser.error(f"--path '{root}' is not an accessible directory.")

    return SearchConfig(
        root     = root,
        pattern  = args.pattern,
        action   = Action(args.action) if args.action else None,
        onfirst  = args.onfirst,
        kind     = TargetKind.DIRECTORY if args.dir else TargetKind.FILE,
    )


def parse_args() -> SearchConfig:
    """Parse simple positional arguments: lookup <path> <pattern> [action] [--onfirst] [--dir]"""
    parser = argparse.ArgumentParser(
        description="Lookup files or directories by pattern, then open or delete them.",
        usage="lookup <path> <pattern> [action] [--onfirst] [--dir]",
        add_help=True,
    )

    parser.add_argument(
        "path",
        metavar="PATH",
        help="Root directory to start searching from.",
    )
    parser.add_argument(
        "pattern",
        metavar="PATTERN",
        help='Glob pattern to match names against, e.g. "*.py" or "test_*".',
    )
    parser.add_argument(
        "action",
        nargs="?",
        choices=[a.value for a in Action],
        default=None,
        help="Optional action: 'open' or 'delete'.",
    )
    parser.add_argument(
        "--onfirst",
        action="store_true",
        help="Apply the action to the very first match found, then stop.",
    )
    parser.add_argument(
        "--dir",
        action="store_true",
        help="Search for directories instead of files.",
    )

    args = parser.parse_args()

    root = Path(args.path)
    if not root.exists():
        parser.error(f"Error: Path '{root}' does not exist.")
    if not root.is_dir():
        parser.error(f"Error: '{root}' is not a directory.")

    return SearchConfig(
        root     = root,
        pattern  = args.pattern,
        action   = Action(args.action) if args.action else None,
        onfirst  = args.onfirst,
        kind     = TargetKind.DIRECTORY if args.dir else TargetKind.FILE,
    )


# ---------------------------------------------------------------------------
# Filesystem walking
# ---------------------------------------------------------------------------

def iter_matches(config: SearchConfig):
    """
    Yield every path under config.root whose name matches config.pattern
    and whose kind (file vs. directory) matches config.kind.
    """
    for dirpath, dirnames, filenames in os.walk(config.root):
        candidates = dirnames if config.kind is TargetKind.DIRECTORY else filenames

        for name in candidates:
            if fnmatch.fnmatch(name, config.pattern):
                yield Path(dirpath) / name


def collect_matches(config: SearchConfig) -> list[Path]:
    """Return all matching paths.  If --onfirst, stop after the first hit."""
    matches = []
    for path in iter_matches(config):
        matches.append(path)
        if config.onfirst:
            break
    return matches


# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------

def open_path(path: Path) -> None:
    """Open a file or directory in the OS default application."""
    try:
        opener = {
            "darwin": ["open"],
            "win32":  ["explorer"],
        }.get(sys.platform, ["xdg-open"])   # Linux / everything else

        subprocess.run([*opener, str(path)], check=False)
        print(f"  Opened: {path}")
    except FileNotFoundError:
        print(f"  Error: Could not open '{path}' — opener not found on this system.")


def delete_path(path: Path) -> None:
    """Delete a file.  For directories, require explicit confirmation."""
    try:
        if path.is_dir():
            answer = input(f"  Delete directory '{path}' and all its contents? [y/N] ")
            if answer.strip().lower() != "y":
                print("  Skipped.")
                return
            import shutil
            shutil.rmtree(path)
        else:
            path.unlink()

        print(f"  Deleted: {path}")
    except PermissionError:
        print(f"  Error: Permission denied — cannot delete '{path}'.")
    except OSError as e:
        print(f"  Error: Failed to delete '{path}' — {e}")


def apply_action(action: Action, path: Path) -> None:
    dispatch = {
        Action.OPEN:   open_path,
        Action.DELETE: delete_path,
    }
    dispatch[action](path)


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

MANY_RESULTS_THRESHOLD = 5


def print_matches(matches: list[Path]) -> None:
    """Print results, collapsing to a count when there are too many."""
    if len(matches) > MANY_RESULTS_THRESHOLD:
        print(f"  Found {len(matches)} matches (too many to list individually).")
    else:
        for path in matches:
            print(f"  {path}")


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------

def run(config: SearchConfig) -> None:
    print(f"\nSearching for {config.kind.value}s matching '{config.pattern}' in '{config.root}' ...\n")

    matches = collect_matches(config)

    if not matches:
        print("No matches found.")
        return

    # ---- --onfirst: act immediately on the single collected match -----------
    if config.onfirst:
        first = matches[0]
        print(f"First match: {first}")
        if config.action:
            apply_action(config.action, first)
        return

    # ---- No --onfirst: decide what to do with the full result list ----------
    if config.action:
        if len(matches) == 1:
            # Unambiguous single result → apply action automatically.
            print(f"Single match found:")
            print_matches(matches)
            print()
            apply_action(config.action, matches[0])
        else:
            # Multiple results → list them; do NOT act (ambiguous).
            print(f"Multiple matches found ({len(matches)} total) — action not applied:\n")
            print_matches(matches)
            print("\nTip: use --onfirst to act on the first match, or narrow your pattern.")
    else:
        # No action requested → just list whatever we found.
        print(f"Matches found ({len(matches)} total):\n")
        print_matches(matches)


def main() -> None:
    config = parse_args()
    run(config)


if __name__ == "__main__":
    main()
