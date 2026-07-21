from pathlib import Path
import shutil

def __check_file_type(file:str|Path)-> Path:
    if not isinstance(file, (str, Path)):
        raise TypeError(f"{type(file).__name__} is not supported")
    return Path(file)


def get_file_extension(file:str|Path) -> str | None:
    file = __check_file_type(file)
    if not file.is_file():
        raise IsADirectoryError(f"{file} is a directory")
    
    return file.suffix
    

def move_into_folder(file:str|Path, folder_name:str) -> str | Path:
    file = __check_file_type(file)

    folder = file.parent / folder_name
    folder.mkdir(exist_ok=True)

    return shutil.move(file, folder)

    

