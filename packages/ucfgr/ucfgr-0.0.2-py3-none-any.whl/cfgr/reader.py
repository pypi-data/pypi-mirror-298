import json
import yaml
from abc import ABC, abstractmethod
from typing import Any


class BaseReader(ABC):
    def __init__(self, file: str):
        self.file = file

    @abstractmethod
    def read(self) -> Any:
        ...

    @abstractmethod
    def write(self, data: Any) -> None:
        ...


class JsonReader(BaseReader):
    def read(self) -> dict:
        with open(self.file, "r", encoding="utf-8") as f:
            return json.load(f)

    def write(self, data: Any) -> None:
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


class YamlReader(BaseReader):
    def read(self) -> dict:
        with open(self.file, "r", encoding="utf-8") as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    def write(self, data: Any) -> None:
        with open(self.file, "w", encoding="utf-8") as f:
            yaml.dump(data, f)
