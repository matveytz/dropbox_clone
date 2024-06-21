import abc

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from files.usecase.repository import AbstractRepository


class AbstractS3(abc.ABC):

    @abc.abstractmethod
    def get_upload_policy(
        self,
        filemetadata_repository: "AbstractRepository",
    ) -> dict[str, str]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_file_download_url(
        self,
        file_id: str,
        filemetadata_repository: "AbstractRepository",
    ) -> str | None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_file_size(self, filename: str, bucket: str) -> int | None:
        raise NotImplementedError
