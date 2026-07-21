from pathlib import Path
from .config import FILE_CATEGORIES, OTHERS
from .utils import get_file_extension, move_into_folder

def _get_file_category(file_extension: str|None) -> str:
    if not file_extension:
        return OTHERS
    
    for category in FILE_CATEGORIES:
        if file_extension in FILE_CATEGORIES[category]:
            return category

    return OTHERS


def organize_folder(folder:Path) -> None:

    for file in folder.iterdir():
        try:
            file_ext = get_file_extension(file)
            file_category = _get_file_category(file_ext)

            move_into_folder(file, file_category)
        except IsADirectoryError:
            continue
