from pathlib import Path
from .config import FILE_CATEGORIES, OTHERS
from .exceptions import InvalidDirectoryError
import shutil


def _validate_file(file:Path) -> None:
    if file.is_dir():
        raise IsADirectoryError(f"{file} is a directory")


def _move_into_folder(file:Path, folder_name:str) -> str | Path:

    folder = file.parent / folder_name
    folder.mkdir(exist_ok=True)

    return shutil.move(file, folder)


def get_file_category(file_extension: str|None) -> str:
    if not file_extension:
        return OTHERS
    
    for category in FILE_CATEGORIES:
        if file_extension in FILE_CATEGORIES[category]:
            return category

    return OTHERS

def organize_folder(folder:Path) -> None:
    try:

        for file in folder.iterdir():
            
            try:

                _validate_file(file)

                file_ext = file.suffix
                file_category = get_file_category(file_ext)

                _move_into_folder(file, file_category)

            except IsADirectoryError:
                continue
            
    except (FileNotFoundError, NotADirectoryError):
        raise InvalidDirectoryError(f"{folder} is not a valid directory")

