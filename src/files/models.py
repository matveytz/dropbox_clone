from django.db import models
from django.conf import settings

from .utils import BaseModel, FileMetadataStatusEnum


class FileMetadataStatus(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField()

    @classmethod
    def get_default_pk(cls):
        return cls.get_or_create_status(FileMetadataStatusEnum.untracked)

    @classmethod
    def get_or_create_status(cls, status: FileMetadataStatusEnum):
        result, created = cls.objects.get_or_create(
            title=status.value[0],
            defaults=dict(description=status.value[1]),
        )
        return result

    def __str__(self) -> str:
        return f'{self.pk}: {self.description}'


class FileMetadata(BaseModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=256)
    extension = models.CharField(max_length=32)
    size_bytes = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_used = models.DateTimeField(auto_now_add=True)
    hash_data = models.CharField(max_length=256)
    minio_key = models.CharField()
    other = models.JSONField(default=list)
    status = models.ForeignKey(
        to=FileMetadataStatus,
        on_delete=models.PROTECT,
        default=FileMetadataStatus.get_default_pk
    )

    def update_status(self, status: FileMetadataStatusEnum):
        self.status = FileMetadataStatus.get_or_create_status(status)
        self.save()

    def get_filename(self) -> str:
        return f'{self.name}{self.extension}'
