import json
from reader.interface import FileReader

class JsonFileReader(FileReader):
    def read(self, file_path: str) -> list[dict]:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)