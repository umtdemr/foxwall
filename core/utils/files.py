import uuid
from os.path import splitext


def generate_new_filename(filename: str) -> str:
    extension = splitext(filename)[1].lower()
    new_filename = str(uuid.uuid4()).replace("-", "") + extension

    return new_filename
