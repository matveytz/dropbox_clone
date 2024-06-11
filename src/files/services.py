from minio import Minio
from django.conf import settings

import uuid


class MinIOService():
    _client = None

    def __init__(self, bucket: str) -> None:
        client = self.get_client()
        if bucket is None:
            self._bucket = settings.MINIO_DEFAULT_BUCKET
        else:
            self._bucket = bucket
        if not client.bucket_exists(self._bucket):
            client.make_bucket(self._bucket, location='ru', object_lock=False)

    def get_client(self) -> Minio:
        if self._client is None:
            self._client = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=False,
            )
        return self._client

    def upload_file(self, file_obj):
        client = self.get_client()
        result = client.put_object(
            bucket_name=self._bucket,
            object_name=uuid.uuid4(),
            data=file_obj,
            length=-1,
            part_size=5*1024*1024,
        )
        return (result.object_name, result.bucket_name, result.last_modified, result.version_id, result.etag)
