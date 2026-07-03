import os

from django.utils.crypto import get_random_string


def path_with_hash(name: str) -> str:
    """
    Encrypting the file upload with ImageField
    or any other fields will use to uploading a file.

    Arguments:
        name (str): The file name will uploaded.
    """
    dir_name, file_name = os.path.split(name)
    file_root, file_ext = os.path.splitext(file_name)
    random = get_random_string(7)
    return os.path.join(dir_name, f"{file_root}_{random}{file_ext}")
