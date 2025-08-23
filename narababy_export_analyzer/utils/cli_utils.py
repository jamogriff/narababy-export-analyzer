import os

def display_success(message: str) -> str:
    print("{0:.<10}{1}".format("[OK]", message))

def display_failure(message: str) -> str:
    print("{0:.<10}{1}".format("[FAIL]", message))


def assert_is_file(file_path: str) -> None:
    """Assert the file is on the filesystem.

    Raises:
        FileNotFoundError: If file does not exist.
    """

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

def get_file_extension(file_path: str) -> str:
    """Return file extension (e.g. .md, .html, .json)"""

    return os.path.splitext(file_path)[1].lower()

def get_valid_csv_from_user() -> str:
    prompt = f"Enter the file path to the Narababy export CSV: "
    file_path = input(prompt)

    assert_is_file(file_path)
    file_extension = get_file_extension(file_path)

    if file_extension != ".csv":
        raise ValueError("File format must be CSV.")

    return file_path
