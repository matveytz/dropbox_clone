from django.db import models
from django.conf import settings

from .enums import FileMetadataStatusEnum
from .constants import DEFAULT_FILEMETADATA_STATUS

import uuid


class BaseModel(models.Model):
    class Meta:
        abstract = True


class BaseModelWithUUID(BaseModel):
    """
    Базовая модель для таблиц с первичным ключом типа UUID
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        abstract = True


class FileMetadataStatusManager(models.Manager):

    def get_status(self, status: FileMetadataStatusEnum) -> 'FileMetadataStatus':
        return self.get_queryset().filter(title=status.name).get()

    def get_default_status(self) -> 'FileMetadataStatus':
        return self.get_status(status=DEFAULT_FILEMETADATA_STATUS)


class FileMetadataStatus(BaseModel):
    title = models.CharField(
        max_length=32,
        unique=True,
        choices=[(k, f.value) for k, f in FileMetadataStatusEnum._member_map_.items()],
    )
    description = models.CharField()

    objects: FileMetadataStatusManager = FileMetadataStatusManager()

    def __str__(self) -> str:
        return f'{self.pk}: {self.description}'


class FileMetadataManager(models.Manager):

    def update_status(self, status: FileMetadataStatusEnum, **filters) -> 'models.QuerySet[FileMetadata]':
        queryset = self.get_queryset().filter(**filters)
        new_status = FileMetadataStatus.objects.get_status(status)
        queryset.update(status=new_status)
        return queryset


class FileMetadata(BaseModelWithUUID):
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
        default=FileMetadataStatus.objects.get_default_status
    )

    objects: FileMetadataManager = FileMetadataManager()

    def get_filename(self) -> str:
        return f'{self.name}{self.extension}'
