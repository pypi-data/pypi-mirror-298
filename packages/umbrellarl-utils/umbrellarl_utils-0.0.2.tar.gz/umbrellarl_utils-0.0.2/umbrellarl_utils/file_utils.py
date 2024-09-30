"""File utilities for UmbrellaRL modules."""

import json

from pathlib import Path

def read_json(path: Path) -> object:
    """
    Load JSON file at provided path.

    Uses utf-8 encoding.
    """
    try:
        with path.open(mode="r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError:
        print(f"Error: The file {path} does not contain valid JSON.")
    except FileNotFoundError:
        print(f"Error: The file {path} was not found.")
    except PermissionError:
        print(f"Error: Permission denied for reading the file {path}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}.")
