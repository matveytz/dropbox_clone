from minio import Minio
from minio.datatypes import PostPolicy
from minio.helpers import BaseURL
from django.conf import settings

from .models import FileMetadata
from .usecase import webhook_hendler, repository, s3
from .utils import get_default_filemetadata
from . import constants

from datetime import timedelta, datetime, timezone
from logging import getLogger
import os


logger = getLogger(__name__)


class FileMetadataRepository(repository.AbstractRepository[FileMetadata]):

    def create(self, **kwargs) -> FileMetadata:
        """
        Если нет kwargs, создается обьект по умолчанию
        """
        if not kwargs:
            kwargs = get_default_filemetadata()
        return FileMetadata.objects.create(**kwargs)

    def get_one(self, pk: str) -> FileMetadata:
        return FileMetadata.objects.filter(id=pk).get()

    def update_one(self, pk, **kwargs) -> FileMetadata:
        queryset = FileMetadata.objects.filter(id=pk)
        queryset.update(**kwargs)
        return queryset.get()


class MinIOService(s3.AbstractS3Service):
    _client = None
    _bucket = None

    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket: str | None = None,
        post_policy_expire: timedelta = constants.DEFAULT_URL_EXPIRE,
    ) -> None:
        if endpoint is None or access_key is None or secret_key is None:
            raise Exception("MinIOService: None arguments")
        self._endpoint = endpoint
        self._access_key = access_key
        self._secret_key = secret_key
        self._post_policy_expire = post_policy_expire
        if bucket is not None:
            self.get_or_create_bucket(bucket)

    def get_or_create_bucket(self, bucket: str):
        self._bucket = str(bucket)
        if not self.client.bucket_exists(self._bucket):
            self.client.make_bucket(self._bucket, location='ru', object_lock=False)

    @property
    def client(self) -> Minio:
        if self._client is None:
            self._client = Minio(
                self._endpoint,
                self._access_key,
                self._secret_key,
                secure=False,
            )
        return self._client

    def _generate_policy(self, expires: timedelta) -> PostPolicy:
        policy = PostPolicy(
            self._bucket, datetime.now(timezone.utc) + expires,
        )
        policy.add_starts_with_condition('key', '')
        policy.add_content_length_range_condition(constants.MIN_FILE_SIZE, constants.MAX_FILE_SIZE)
        return policy

    def get_upload_policy(
        self,
        filemetadata_repository: repository.AbstractRepository = FileMetadataRepository(),
    ) -> dict[str, str]:
        instance = filemetadata_repository.create()
        self.get_or_create_bucket(instance.pk)
        url = self.client._base_url
        if settings.DEBUG:
            url = constants.DEBAG_URL
        policy_data = {
            'url': f'{url}/{self._bucket}/',
            'bucket': f'{self._bucket}',
            'creds': self.client.presigned_post_policy(self._generate_policy(self._post_policy_expire))
        }
        return policy_data

    def get_file_download_url(
        self,
        file_id: str,
        filemetadata_repository: repository.AbstractRepository = FileMetadataRepository(),
        expires: timedelta = constants.DEFAULT_URL_EXPIRE,
    ) -> str | None:
        instance: FileMetadata = filemetadata_repository.get_one(file_id)
        self._bucket = str(instance.pk)
        if not self.client.bucket_exists(self._bucket) or not self.client.list_objects(self._bucket):
            return None
        if settings.DEBUG:
            self.client._base_url = BaseURL(constants.DEBAG_URL, self.client._base_url._region)
        return self.client.presigned_get_object(
            bucket_name=self._bucket,
            object_name=instance.get_filename(),
            expires=expires,
        )

    def get_file_size(self, filename: str, bucket: str | None) -> int | None:
        self._bucket = bucket
        if self._bucket is None:
            return None
        stat_file = self.client.stat_object(self._bucket, filename)
        return stat_file.size


class MinIOWebhookService(webhook_hendler.WebhookHandler):

    def get_mapping_key(self, webhook_data) -> str | None:
        try:
            if webhook_data['api']['statusCode'] != 200:
                return None
            webhook_name = webhook_data['api']['name']
            if webhook_name not in self.method_handle_mapping:
                return None
            return webhook_name
        except KeyError:
            logger.error(f"Invalid webhook data: {webhook_data}")
            raise

    def post_policy_bucket_handler(
        self,
        webhook_data,
        filemetadata_repository: repository.AbstractRepository,
        s3_service: s3.AbstractS3Service
    ) -> None:
        try:
            file_name, file_extension = os.path.splitext(webhook_data['tags']['objectLocation']['name'])
            bucket = webhook_data['api']['bucket']
            file_hash = webhook_data['responseHeader']['ETag']
            minio_key = f"{webhook_data['api']['bucket']}/{file_name}{file_extension}"
            file_size_bytes = s3_service.get_file_size(file_name + file_extension, bucket)
            now = datetime.now(timezone.utc)
        except KeyError:
            logger.error(f"Invalid event data: {webhook_data}")
            raise
        filemetadata_repository.update_one(
            pk=bucket,
            name=file_name,
            extension=file_extension,
            size_bytes=file_size_bytes,
            hash_data=file_hash,
            minio_key=minio_key,
            updated_at=now,
            last_used=now,
        )

    method_handle_mapping = {
        'PostPolicyBucket': post_policy_bucket_handler
    }
