import os


def path_exists(file_path: str) -> None:

    # Extract the directory path
    directory = os.path.dirname(file_path)

    # Check if the directory exists, and if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

def has_file_modified(file_path: str, original_mod_time) -> bool:
    current_mod_time = os.path.getmtime(file_path)
    return current_mod_time != original_mod_time

def file_empty(file_path: str) -> bool:
    return os.path.getsize(file_path) == 0

def extensions(file_path: str) -> list[str]:
    abs_path = os.path.abspath(file_path)
    base, ext = os.path.splitext(abs_path)

    # Loop to get all extensions
    extensions = [ext]
    while True:
        base, ext = os.path.splitext(base)
        if ext:
            extensions.append(ext)
        else:
            break

    extensions.reverse()  # To maintain the original order
    
    return extensions