import abc
from typing import Any, Type, TypeVar

from . import mixins


class ServiceConfig(mixins.EnvConfigMixin, abc.ABC):
    @property
    @abc.abstractmethod
    def url(self) -> str:
        ...


SingletonClass = TypeVar("SingletonClass")


class SingletonMeta(type):
    _instances: dict[Type[SingletonClass], SingletonClass] = {}

    def __call__(cls, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> SingletonClass:
        instance: SingletonClass = cls._instances.setdefault(cls, super().__call__(*args, **kwargs))
        return instance
