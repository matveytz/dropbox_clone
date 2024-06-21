from files.usecase.webhook_handler import WebhookHandler
from files.services.filemetadata_repository import filemetadata_repository_factory
from files.services.minio_facade import s3_factory

from datetime import datetime, timezone
from logging import getLogger
import os

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from files.usecase.repository import AbstractRepository
    from files.usecase.s3 import AbstractS3


logger = getLogger(__name__)


class MinIOWebhookService(WebhookHandler):

    def get_mapping_key(self, webhook_data) -> str | None:
        """
        Возвращает ключ словаря method_handle_mapping
        Значение в словаре по этому ключу, будет обрабатывать текущий вебхук
        Если возвращает None, webhook_data передается обработчику по умолчанию default_handler
        """
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
        filemetadata_repository: "AbstractRepository" = filemetadata_repository_factory(),
        s3_service: "AbstractS3" = s3_factory(),
    ) -> None:
        """
        Обработчик для PostPolicyBucket: пользователь загружает файл Post запросом на сервис MinIO.
        Обновляет поля в Filemetadata.
        """
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


def webhook_service_factory():
    return MinIOWebhookService()
