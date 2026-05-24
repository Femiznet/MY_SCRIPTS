"""
Entry point for running lookup from the command line.

Usage:
    python -m lookup <path> <pattern> [action] [--onfirst] [--dir]
    lookup <path> <pattern> [action] [--onfirst] [--dir]

Examples:
    lookup . "*.py"
    lookup ./src "test_*.py" open --onfirst
    lookup ./logs "*.log" delete --onfirst
    lookup . "node_modules" --dir
"""

from lookup import main

if __name__ == "__main__":
    main()
