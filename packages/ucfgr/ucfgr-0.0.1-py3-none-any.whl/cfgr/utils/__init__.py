from typing import Any, Self, Literal, Generic, TypeVar
from dataclasses import dataclass
from abc import ABC


T = TypeVar("T")


@dataclass
class SubConfigRef:
    cfg_type: "cfgr.manager.BaseConfig"
    cfg_format: Literal["json", "yaml"] = "json"
    cfg_json: dict = None
    cfg_yaml: dict = None
    cfg_file: str = None


class ProInjector:
    def __init__(self, cls: Any):
        self.cls = cls

    def inject(self, name: str, value: Any, type_of: Any = Any) -> Self:
        if type_of is not Any and not isinstance(value, type_of):
            try:
                value = type_of(value)
            except TypeError:
                value = value

        if isinstance(value, SubConfigRef):
            if value.cfg_format == "json":
                if value.cfg_json is None:
                    value = value.cfg_type.json_load_from(value.cfg_file)
                else:
                    value = value.cfg_type(**value.cfg_json)
            elif value.cfg_format == "yaml":
                value = value.cfg_type.yaml_build_from(value.cfg_file)
        elif isinstance(value, dict) and not isinstance(type_of, dict):
            try:
                value = type_of(**value)
            except TypeError:
                value = value

        setattr(self.cls, name, value)
        return self


class BaseMappingV(Generic[T]):
    def __init__(self, value: T):
        self.value: T = value
        self.checker = type(self)

    def check(self, obj: Any) -> bool:
        return isinstance(obj, self.checker)


class Mapping(ABC):
    def __init_subclass__(cls, **kwargs):
        for i in cls.__annotations__:
            if i not in cls.__dict__:
                setattr(cls, i, type(i, (BaseMappingV,), {})(value=None))
            else:
                setattr(cls, i, type(i, (BaseMappingV,), {})(value=getattr(cls, i)))
