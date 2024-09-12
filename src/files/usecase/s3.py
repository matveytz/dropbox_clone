import abc


class AbstractS3(abc.ABC):

    @abc.abstractmethod
    def get_upload_policy(
        self,
        new_bucket: str,
    ) -> dict[str, str]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_file_download_url(
        self,
        file_id: str,
        filename: str,
    ) -> str | None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_file_size(self, filename: str, bucket: str) -> int | None:
        raise NotImplementedError
