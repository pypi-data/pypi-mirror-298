from abc import ABC
from typing import Self, Optional

from .utils import ProInjector, BaseMappingV, Mapping
from .reader import JsonReader, YamlReader, BaseReader


class Serializers(Mapping):
    JSON: BaseMappingV = JsonReader
    YAML: BaseMappingV = YamlReader


class BaseConfig(ABC):
    _loaded_cfgs: dict = {}
    _anns: dict
    reader: BaseReader = None

    def __init__(self, **kwargs):
        self.custom_pre(**kwargs)

        injector = ProInjector(self)
        for i in kwargs:
            if i in list(self._anns.keys()):
                injector.inject(i, kwargs[i], self._anns[i])

        self.custom_post(**kwargs)

    def __init_subclass__(cls, **kwargs):
        cls._anns = cls.__annotations__

    def custom_pre(self, **kwargs):
        pass

    def custom_post(self, **kwargs):
        pass

    def dump_pre(self):
        pass

    @classmethod
    def load_from(cls, file_name: str, serializer: BaseMappingV, key: Optional[str] = None) -> Self:
        cls.reader: BaseReader = serializer.value(file_name)
        cfg = cls(**(cls.reader.read()))
        cls._loaded_cfgs[key] = cfg
        return cfg

    @classmethod
    def create(cls) -> dict:
        cfg = {}
        for i in cls._anns:
            if cls._anns.get(i) is str:
                cfg[i] = ""
            elif cls._anns.get(i) in [int, float]:
                cfg[i] = 0
            elif cls._anns.get(i) is list:
                cfg[i] = []
            elif cls._anns.get(i) is dict:
                cfg[i] = {}
            else:
                if issubclass(cls._anns.get(i), BaseConfig):
                    cfg[i] = cls._anns.get(i).create()

        return cfg

    @classmethod
    def create_and_write(cls, file_name: str, serializer: BaseMappingV) -> None:
        reader: BaseReader = serializer.value(file_name)
        reader.write(cls.create())

    @classmethod
    def get(cls, key: str):
        if key in cls._loaded_cfgs:
            return cls._loaded_cfgs[key]
        else:
            return None

    def dump(self) -> dict:
        cfg = {}
        for i in self._anns:
            if issubclass(type(self.__dict__.get(i)), BaseConfig):
                cfg[i] = self.__dict__.get(i).dump()
            elif self._anns.get(i) in [str, int, float, list, dict]:
                cfg[i] = self.__dict__.get(i)

        return cfg

    def write(self, file_name: Optional[str] = None, serializer: Optional[BaseMappingV] = None) -> None:
        if self.reader is not None:
            self.reader.write(self.dump())
        else:
            reader: BaseReader = serializer.value(file_name)
            reader.write(self.dump())
