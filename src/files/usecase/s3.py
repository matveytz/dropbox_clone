import abc


class AbstractS3Service(abc.ABC):

    @abc.abstractmethod
    def get_file_download_url():
        raise NotImplementedError

    @abc.abstractmethod
    def get_upload_policy():
        raise NotImplementedError
