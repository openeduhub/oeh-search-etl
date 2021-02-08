from abc import ABCMeta, abstractmethod
from typing import Type, TypeVar
_T = TypeVar('_T')


class SpiderBase(ABCMeta):
    @classmethod
    @property
    @abstractmethod
    def name(cls):
        pass

    @classmethod
    @property
    @abstractmethod
    def version(cls):
        pass

    @classmethod
    @property
    @abstractmethod
    def friendlyName(cls):
        pass

    @classmethod
    @property
    @abstractmethod
    def url(cls):
        pass

    def register(cls: ABCMeta, subclass: Type[_T]) -> Type[_T]:
        print(cls, subclass)
        return super().register(subclass)



