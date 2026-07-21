import pytest
from unittest.mock import patch
from pathlib import Path
from src.lib import organizer, cli, utils


def test_cli_args(tmp_path):
    target = tmp_path / "test_files"
    target.mkdir()
    with patch("sys.argv", ["script.py", str(target)]):
        assert cli.get_directory() == target


def test_invalid_directory():
    with patch("sys.argv", ["script.py", "nonexistent_folder"]):
        with pytest.raises(NotADirectoryError):
            cli.get_directory()


@pytest.mark.parametrize("filename,expected", [
    ("test.txt", ".txt"),
    ("archive.tar.gz", ".gz"),
    ("no_extension", "")
])
def test_get_file_extension(tmp_path, filename, expected):
    f = tmp_path / filename
    f.touch()
    assert utils.get_file_extension(f) == expected


def test_directory_extension(tmp_path):
    folder = tmp_path / "directory"
    folder.mkdir()
    with pytest.raises(IsADirectoryError):
        utils.get_file_extension(folder)


def test_move_into_folder(tmp_path):
    f = tmp_path / "test.txt"
    f.touch()
    moved = utils.move_into_folder(f, "docs")
    assert Path(moved).parent.name == "docs"
    assert Path(moved).exists()


def test_organize_folder(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.touch()
    organizer.organize_folder(tmp_path)
    assert not (tmp_path / "sample.txt").exists()
    assert (tmp_path / "Documents" / "sample.txt").exists()


def test_directory_only_folder(tmp_path):
    folder = tmp_path / "directory"
    folder.mkdir()
    organizer.organize_folder(tmp_path)

    assert not (tmp_path / "Others" / "directory").exists()