from abc import ABCMeta, abstractmethod


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



