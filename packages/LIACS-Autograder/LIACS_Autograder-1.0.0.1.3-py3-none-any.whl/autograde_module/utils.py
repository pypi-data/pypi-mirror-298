from pathlib import Path
import os

def get_txt_path(filename, extend=""):
    """
    Create the file path for the report files (.txt)
    Reports have the same filename as the Python code of students.
    """
    dir_ = Path(filename).parents[0]
    path = dir_ / Path(filename).stem
    if extend:
        path = path.with_name(f"{path.stem}_{extend}")
    return path.with_suffix('.txt')

def find_relative_import(import_file):
    """
    This finds the common parent of two file paths.
    Next, it determines the import path for import_file depending on main_file.
    :type import_file: str or Path
    :rtype: Path
    """
    main_file, import_file = Path(os.getcwd()), Path(import_file)

    for parent in main_file.parents:
        try:
            path = import_file.relative_to(parent)
        except ValueError:
            continue
        return path.with_suffix('').as_posix().replace("/", ".").split(".", 1)[1]
    raise ValueError(f"No common parent directory could be found for {main_file} and {import_file}!")