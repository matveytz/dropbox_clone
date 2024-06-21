import abc
from typing import TypeVar, Generic


T = TypeVar('T')


class AbstractRepository(abc.ABC, Generic[T]):
    @abc.abstractmethod
    def create(self, **kwargs) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    def get_one(self, pk: str) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    def update_one(sself, pk: str, **kwargs) -> T:
        raise NotImplementedError
