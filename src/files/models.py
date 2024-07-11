from django.db import models
from django.conf import settings

from .enums import FileMetadataStatusEnum
from .constants import DEFAULT_FILEMETADATA_STATUS

import uuid


class BaseModel(models.Model):
    """
    Базовая модель для таблиц с первичным ключом типа UUID
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        abstract = True


class FileMetadataStatus(models.Model):
    title = models.CharField(
        max_length=32,
        unique=True,
        choices=[(k, f.value) for k, f in FileMetadataStatusEnum._member_map_.items()],
    )
    description = models.CharField()

    @classmethod
    def get_default_status(cls) -> "FileMetadataStatus":
        return cls.get_or_create_status(DEFAULT_FILEMETADATA_STATUS)

    @classmethod
    def get_or_create_status(cls, status: FileMetadataStatusEnum) -> "FileMetadataStatus":
        result, created = cls.objects.get_or_create(
            title=status.name,
            defaults=dict(description=status.value),
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
    hash_data = models.CharField(max_length=256)
    minio_key = models.CharField()
    other = models.JSONField(default=list)
    status = models.ForeignKey(
        to=FileMetadataStatus,
        on_delete=models.PROTECT,
        default=FileMetadataStatus.get_default_status
    )

    def update_status(self, status: FileMetadataStatusEnum):
        self.status = FileMetadataStatus.get_or_create_status(status)
        self.save()

    def get_filename(self) -> str:
        return f'{self.name}{self.extension}'
