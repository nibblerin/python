import json
from pathlib import Path

from reader.interface import FileReader


class JsonFileReader(FileReader):
    def read(self, file_path: str | Path) -> list[dict]:
        path = Path(file_path)
        try:
            with path.open("r", encoding="utf-8") as file:
                return json.load(file)
            
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found or path is not a file: {path}")
        except PermissionError:
            raise PermissionError(f"Permission denied to read file: {path}")
        except UnicodeDecodeError as e:
            raise ValueError(f"Encoding error while reading file {path}: {e}") from e
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON syntax in file {path}: {e}") from e