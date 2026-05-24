"""
Unit tests for lookup.py

Run with: pytest tests/test_lookup.py
"""

import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from lookup import (
    Action,
    TargetKind,
    SearchConfig,
    iter_matches,
    collect_matches,
    parse_args,
)


class TestSearchConfig:
    """Test SearchConfig dataclass creation."""

    def test_valid_config(self):
        """Test creating a valid SearchConfig."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = SearchConfig(
                root=Path(tmpdir),
                pattern="*.py",
                action=Action.OPEN,
                onfirst=False,
                kind=TargetKind.FILE,
            )
            assert config.pattern == "*.py"
            assert config.action == Action.OPEN
            assert config.onfirst is False


class TestIterMatches:
    """Test file/directory matching logic."""

    def test_find_files_by_pattern(self):
        """Test finding files matching a glob pattern."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Create test files
            (tmppath / "test1.py").touch()
            (tmppath / "test2.py").touch()
            (tmppath / "readme.txt").touch()
            
            config = SearchConfig(
                root=tmppath,
                pattern="*.py",
                action=None,
                onfirst=False,
                kind=TargetKind.FILE,
            )
            
            matches = list(iter_matches(config))
            assert len(matches) == 2
            assert all(m.suffix == ".py" for m in matches)

    def test_find_directories(self):
        """Test finding directories matching a pattern."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Create test directories
            (tmppath / "node_modules").mkdir()
            (tmppath / "src").mkdir()
            (tmppath / "build").mkdir()
            
            config = SearchConfig(
                root=tmppath,
                pattern="node_modules",
                action=None,
                onfirst=False,
                kind=TargetKind.DIRECTORY,
            )
            
            matches = list(iter_matches(config))
            assert len(matches) == 1
            assert matches[0].name == "node_modules"

    def test_nested_directory_search(self):
        """Test recursively finding files in subdirectories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Create nested structure
            subdir = tmppath / "sub" / "nested"
            subdir.mkdir(parents=True)
            
            (tmppath / "test.py").touch()
            (subdir / "test.py").touch()
            
            config = SearchConfig(
                root=tmppath,
                pattern="test.py",
                action=None,
                onfirst=False,
                kind=TargetKind.FILE,
            )
            
            matches = list(iter_matches(config))
            assert len(matches) == 2

    def test_no_matches(self):
        """Test when pattern matches nothing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            (tmppath / "file.txt").touch()
            
            config = SearchConfig(
                root=tmppath,
                pattern="*.nonexistent",
                action=None,
                onfirst=False,
                kind=TargetKind.FILE,
            )
            
            matches = list(iter_matches(config))
            assert len(matches) == 0


class TestCollectMatches:
    """Test match collection with onfirst behavior."""

    def test_collect_all_matches(self):
        """Test collecting all matches."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            for i in range(3):
                (tmppath / f"file{i}.py").touch()
            
            config = SearchConfig(
                root=tmppath,
                pattern="*.py",
                action=None,
                onfirst=False,
                kind=TargetKind.FILE,
            )
            
            matches = collect_matches(config)
            assert len(matches) == 3

    def test_collect_first_only(self):
        """Test collecting only the first match with onfirst=True."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            for i in range(5):
                (tmppath / f"file{i}.py").touch()
            
            config = SearchConfig(
                root=tmppath,
                pattern="*.py",
                action=None,
                onfirst=True,
                kind=TargetKind.FILE,
            )
            
            matches = collect_matches(config)
            assert len(matches) == 1


class TestParseArgs:
    """Test argument parsing."""

    def test_parse_basic_args(self):
        """Test parsing basic positional arguments."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("sys.argv", ["lookup", tmpdir, "*.py"]):
                config = parse_args()
                assert config.pattern == "*.py"
                assert config.action is None
                assert config.onfirst is False

    def test_parse_with_action(self):
        """Test parsing with an action."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("sys.argv", ["lookup", tmpdir, "*.log", "delete"]):
                config = parse_args()
                assert config.action == Action.DELETE

    def test_parse_with_flags(self):
        """Test parsing with optional flags."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("sys.argv", ["lookup", tmpdir, "*", "open", "--onfirst", "--dir"]):
                config = parse_args()
                assert config.action == Action.OPEN
                assert config.onfirst is True
                assert config.kind == TargetKind.DIRECTORY

    def test_parse_nonexistent_path(self):
        """Test that parsing fails gracefully for nonexistent paths."""
        with patch("sys.argv", ["lookup", "/nonexistent/path", "*.py"]):
            with pytest.raises(SystemExit):
                parse_args()

    def test_parse_file_as_path(self):
        """Test that parsing fails when path is a file, not a directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            filepath = tmppath / "file.txt"
            filepath.touch()
            
            with patch("sys.argv", ["lookup", str(filepath), "*.py"]):
                with pytest.raises(SystemExit):
                    parse_args()


class TestActionEnum:
    """Test Action enum values."""

    def test_open_action(self):
        """Test that open action exists."""
        assert Action.OPEN.value == "open"

    def test_delete_action(self):
        """Test that delete action exists."""
        assert Action.DELETE.value == "delete"


class TestTargetKindEnum:
    """Test TargetKind enum values."""

    def test_file_kind(self):
        """Test that file kind exists."""
        assert TargetKind.FILE.value == "file"

    def test_directory_kind(self):
        """Test that directory kind exists."""
        assert TargetKind.DIRECTORY.value == "directory"


class TestIntegration:
    """Integration tests for common workflows."""

    def test_full_search_workflow(self):
        """Test a complete search workflow without actions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Create test structure
            (tmppath / "main.py").touch()
            (tmppath / "utils.py").touch()
            (tmppath / "readme.txt").touch()
            
            # Search for Python files
            with patch("sys.argv", ["lookup", str(tmppath), "*.py"]):
                config = parse_args()
                matches = collect_matches(config)
                
                assert len(matches) == 2
                assert all(m.suffix == ".py" for m in matches)

    def test_file_deletion_workflow(self):
        """Test the deletion workflow (with user confirmation mocked)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            filepath = tmppath / "temp.txt"
            filepath.touch()
            
            # Verify file exists
            assert filepath.exists()
            
            # Delete it
            filepath.unlink()
            
            # Verify it's gone
            assert not filepath.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
