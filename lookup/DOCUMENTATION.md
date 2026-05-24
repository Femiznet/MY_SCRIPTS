# Lookup Package Documentation

## Overview

`Lookup` is a cross-platform CLI utility for searching files and directories by pattern, with optional actions to open or delete matches. It's designed to be simple, extensible, and installable via pip.

---

## Installation

### Option 1: Install from Local Development

Navigate to the path where lookup folder is.
```bash
cd /path/to/lookup
pip install -e .
```

### Option 2: Install from PyPI
```bash
pip install lookup
```

After installation, use it from **anywhere**:
```bash
lookup [path] [pattern] [action] [options]
```

---

## Usage

### Basic Syntax
```bash
lookup [path] [pattern] [action] [--onfirst] [--dir]
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `<path>` | Yes | Root directory to search from (e.g., `.`, `./src`, `/home/user/projects`) |
| `<pattern>` | Yes | Glob pattern to match (e.g., `*.py`, `test_*`, `README*`) |
| `[action]` | No | Action to perform: `open` or `delete` |
| `--onfirst` | No | Apply action to first match only, then stop |
| `--dir` | No | Search for directories instead of files |

### Examples

#### Lookup all Python files
```bash
# Output: Lists all `.py` files in current directory and subdirectories
lookup . "*.py"
```


#### Lookup test files and open the first one
```bash
# Opens the first matching file in your default application
lookup ./src "test_*.py" open --onfirst
```


#### Lookup log files
```bash
# Lists all `.log` files without taking action
lookup ./logs "*.log"
```


#### Lookup and delete the first log file
```bash
# Deletes only the first match (with confirmation for directories)
lookup ./logs "*.log" delete --onfirst
```

#### Search for directories
```bash
# Lists all `node_modules` directories
lookup . "node_modules" --dir
```

#### Lookup README files
```bash
lookup /path/to/project "README*"
```

---

## Behavior

```bash
    --action
```
### Without Action 
Simply lists all matching files/directories.

### With Action (Single Match)
If exactly one match is found and an action is specified, the action is **applied automatically** without confirmation (unless it's a directory deletion).

### With Action (Multiple Matches)
If multiple matches exist and an action is specified:
- The action is **NOT applied** (- too many files to perform an action on)
- Use `--onfirst` to target the first match instead

### Directory Deletion
When deleting a directory, you must confirm with `y` at the prompt.

---

## How It Works Internally

### Package Structure
```
lookup/
├── __main__.py       # Entry point for module execution
├── lookup.py         # Core logic (DO NOT MODIFY for extensions)
├── setup.py          # Pip installation metadata
└── DOCUMENTATION.md  # This file
```

### Core Components (in `lookup.py`)

1. **Domain Types**
   - `Action`: `open` or `delete`
   - `TargetKind`: `file` or `directory`
   - `SearchConfig`: Dataclass holding validated search parameters

2. **Argument Parsing** (`parse_args()`)
   - Converts CLI arguments to `SearchConfig`
   - Validates that the root path exists and is a directory

3. **Filesystem Walking** (`iter_matches()`, `collect_matches()`)
   - Recursively walks directory tree
   - Matches names against glob pattern
   - Returns matching paths as a list

4. **Actions** (`open_path()`, `delete_path()`, `apply_action()`)
   - `open_path`: Uses OS-specific opener (explorer, open, xdg-open)
   - `delete_path`: Deletes files or directories (with confirmation for dirs)

5. **Output** (`print_matches()`)
   - Lists results or shows count if too many (>5)

6. **Main Orchestration** (`run()`, `main()`)
   - Coordinates the workflow
   - Decides when to apply actions based on match count and flags

---

## Extending the Package

The logic is intentionally kept simple and self-contained in `lookup.py`. To add new features:

### Add a New Action

1. **Open `lookup.py`** and add to the `Action` enum:
```python
class Action(str, Enum):
    OPEN   = "open"
    DELETE = "delete"
    YOUR_ACTION = "your_action"  # Add here
```

2. **Implement the action function**:
```python
def your_action_path(path: Path) -> None:
    """Your custom action logic."""
    print(f"  Custom action on: {path}")
```

3. **Register in `apply_action()`**:
```python
def apply_action(action: Action, path: Path) -> None:
    dispatch = {
        Action.OPEN:   open_path,
        Action.DELETE: delete_path,
        Action.YOUR_ACTION: your_action_path,  # Add here
    }
    dispatch[action](path)
```

4. **Update the argparser choices** in `parse_args()`:
```python
parser.add_argument(
    "action",
    nargs="?",
    choices=[a.value for a in Action],  # Automatically includes new action
    ...
)
```

### Add a New Search Type

1. **Add to `TargetKind` enum** if needed
2. **Update `iter_matches()`** to handle the new type
3. **Update `parse_args()`** with a new flag if needed

### Example: Add a "copy" Action
```python
# 1. Add to enum
class Action(str, Enum):
    COPY = "copy"

# 2. Implement function
def copy_path(path: Path) -> None:
    """Copy to clipboard."""
    import shutil
    if path.is_dir():
        # handle directory
        pass
    shutil.copy(path, "/tmp/clipboard")
    print(f"  Copied to clipboard: {path}")

# 3. Register in dispatch
dispatch = {
    ...,
    Action.COPY: copy_path,
}
```

Usage after extension:
```bash
lookup ./docs "*.pdf" copy --onfirst
```

---

## Installation via Pip (Setup)

The `setup.py` file defines:
- **Package name**: `lookup-utility`
- **Entry point**: `lookup` command globally available
- **Version**: Auto-detected from git tags or manual specification

After `pip install -e .`, you can run:
```bash
lookup . "*.py"
```

From **any directory** on your system.

---

## Platform Support

- **Linux**: Uses `xdg-open`
- **macOS**: Uses `open`
- **Windows**: Uses `explorer`

---

## Common Workflows

### Clean Up Old Logs
```bash
lookup ./logs "*.log" delete --onfirst
```

### Lookup All TODO Comments (by filename)
```bash
lookup ./src "*TODO*"
```

### Batch Open Config Files
```bash
lookup /etc "*.conf" open
```

### Locate and Delete Temporary Files
```bash
lookup . "*.tmp" delete
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Command not found | Run `pip install -e .` from package directory |
| Pattern matches nothing | Double-check glob syntax (e.g., `*.py` not `*.py*`) |
| Action not applied | Check if multiple matches exist (use `--onfirst` to target first) |
| Permission denied on delete | Run with appropriate permissions or check file ownership |

---

## Features

- **Positional args**: `lookup [path] [pattern] [action] [--flags]`
- **Simple extensions**: Just edit `lookup.py` to add new actions
- **Core logic untouched**: All the search/filter logic remains intact
- **Cross-platform**: Works on Windows, macOS, Linux
- **Smart actions**: Won't delete multiple matches without `--onfirst`

The `DOCUMENTATION.md` has everything you need to understand and extend it!
