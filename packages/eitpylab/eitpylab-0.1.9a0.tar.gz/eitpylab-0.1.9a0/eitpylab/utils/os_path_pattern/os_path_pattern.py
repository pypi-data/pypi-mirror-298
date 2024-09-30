from pathlib import Path


def set_absolute_path(path):
    try:
        return Path(path).resolve()
    except Exception as exc:
        print(exc)
