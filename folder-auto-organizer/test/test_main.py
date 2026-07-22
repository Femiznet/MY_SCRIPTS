import pytest
from unittest.mock import patch
from src.lib import organizer, cli
from src.lib.exceptions import InvalidDirectoryError

sample_directory = "sample_driectory"
sample_file = "sample.txt"

def test_cli_args_for_valid_directory(tmp_path):
    directory = tmp_path / sample_directory
    directory.mkdir()

    with patch("sys.argv", ["script.py", str(directory)]):
        assert cli.get_directory() == directory


def test_cli_args_for_invalid_directory(tmp_path):
    directory = tmp_path / sample_directory

    with patch("sys.argv", ["script.py", str(directory)]):
        with pytest.raises(NotADirectoryError):
            cli.get_directory()


def test_organize_folder_of_files(tmp_path):
    file_path = tmp_path / sample_file
    file_path.touch()

    organizer.organize_folder(tmp_path)
    assert not (tmp_path / sample_file).exists()

    file_ext = file_path.suffix
    category = organizer.get_file_category(file_ext)
    assert (tmp_path / category / sample_file).exists()

def test_organize_folder_of_directories(tmp_path):
    directory = tmp_path / sample_directory
    directory.mkdir()

    organizer.organize_folder(tmp_path)
    assert (tmp_path / directory).exists()


def test_organize_folder_of_invalid_path(tmp_path):
    folder = tmp_path / sample_directory

    with pytest.raises(InvalidDirectoryError):
        organizer.organize_folder(folder)

    folder.touch()

    with pytest.raises(InvalidDirectoryError):
        organizer.organize_folder(folder)
    