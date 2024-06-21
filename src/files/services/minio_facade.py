from minio import Minio
from minio.datatypes import PostPolicy
from minio.helpers import BaseURL
from django.conf import settings

from files.usecase.s3 import AbstractS3
from files.constants import (
    DEFAULT_CONNECTION_TIMEOUT,
    DEFAULT_URL_EXPIRE,
    MIN_FILE_SIZE,
    MAX_FILE_SIZE,
    MINIO_DEBAG_URL,
)

from datetime import timedelta, datetime, timezone
from logging import getLogger
import urllib3


logger = getLogger(__name__)


class MinIOFacade(AbstractS3):
    __client: Minio | None = None

    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        post_policy_expire: timedelta = DEFAULT_URL_EXPIRE,
        http_client: urllib3.PoolManager | None = None,
    ) -> None:
        if endpoint is None or access_key is None or secret_key is None:
            raise Exception("MinIOService: None arguments")
        self._endpoint = endpoint
        self._access_key = access_key
        self._secret_key = secret_key
        self._post_policy_expire = post_policy_expire
        self._http_client = http_client or self._get_default_http_client()

    @property
    def _client(self):
        """
        Бросает исключение MinioException при первом вызове, если нет подключения к MinIO
        """
        if self.__client is None:
            self.__client = Minio(
                self._endpoint,
                self._access_key,
                self._secret_key,
                secure=False,
                http_client=self._http_client,
            )
            self.__client.list_buckets()
        return self.__client

    @staticmethod
    def _get_default_http_client() -> urllib3.PoolManager:
        return urllib3.PoolManager(
            timeout=urllib3.Timeout(connect=DEFAULT_CONNECTION_TIMEOUT, read=DEFAULT_CONNECTION_TIMEOUT),
            maxsize=10,
            cert_reqs='CERT_NONE',
            retries=urllib3.Retry(
                total=5,
                backoff_factor=0.2,
                status_forcelist=[500, 502, 503, 504]
            )
        )

    @staticmethod
    def _generate_policy(bucket: str, expires: timedelta) -> PostPolicy:
        policy = PostPolicy(
            bucket, datetime.now(timezone.utc) + expires,
        )
        policy.add_starts_with_condition('key', '')
        policy.add_content_length_range_condition(MIN_FILE_SIZE, MAX_FILE_SIZE)
        return policy

    def _create_bucket(self, bucket: str) -> None:
        if not self._client.bucket_exists(bucket):
            self._client.make_bucket(bucket, location='ru', object_lock=False)

    def get_upload_policy(
        self,
        new_bucket: str,
    ) -> dict[str, str]:
        self._create_bucket(new_bucket)
        url = self._client._base_url
        if settings.DEBUG:
            url = MINIO_DEBAG_URL
        policy_data = {
            'url': f'{url}/{new_bucket}/',
            'creds': self._client.presigned_post_policy(
                self._generate_policy(
                    new_bucket,
                    self._post_policy_expire,
                )
            )
        }
        return policy_data

    def get_file_download_url(
        self,
        file_id: str,
        filename: str,
    ) -> str | None:
        if not self._client.bucket_exists(file_id) or not self._client.list_objects(file_id):
            return None
        if settings.DEBUG:
            self._client._base_url = BaseURL(MINIO_DEBAG_URL, self._client._base_url._region)
        return self._client.presigned_get_object(
            bucket_name=file_id,
            object_name=filename,
            expires=self._post_policy_expire,
        )

    def get_file_size(self, filename: str, bucket: str) -> int | None:
        stat_file = self._client.stat_object(bucket, filename)
        return stat_file.size


def s3_factory() -> MinIOFacade:
    return MinIOFacade(
        endpoint=settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
    )
