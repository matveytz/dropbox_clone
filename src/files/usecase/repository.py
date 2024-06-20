import abc
from typing import TypeVar, Generic


T = TypeVar('T')


class AbstractRepository(abc.ABC, Generic[T]):
    @abc.abstractmethod
    def create(self, *args, **kwargs) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    def get_one(self, *args, **kwargs) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    def update_one(self, *args, **kwargs) -> T:
        raise NotImplementedError
