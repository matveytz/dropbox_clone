from django.contrib.auth import get_user_model

from files.usecase.repository import AbstractRepository
from files.models import FileMetadata
from files.enums import FileMetadataStatusEnum
from files.constants import DEFAULT_FILEMETADATA_SCHEMA


class FileMetadataRepository(AbstractRepository[FileMetadata]):

    def create(self, **kwargs) -> FileMetadata:
        """
        Если нет kwargs, создается обьект по умолчанию
        """
        if not kwargs:
            kwargs = DEFAULT_FILEMETADATA_SCHEMA.copy()
            kwargs["owner"] = get_user_model().objects.all().order_by('id').first()
        return FileMetadata.objects.create(**kwargs)

    def get_one(self, pk: str) -> FileMetadata:
        return FileMetadata.objects.filter(id=pk).get()

    def update_one(self, pk: str, **kwargs) -> FileMetadata:
        queryset = FileMetadata.objects.filter(id=pk)
        status = kwargs.pop('status', None)
        queryset.update(**kwargs)
        if status and isinstance(status, FileMetadataStatusEnum):
            FileMetadata.objects.update_status(status, pk=pk)
        return queryset.get()


def filemetadata_repository_factory():
    return FileMetadataRepository()
