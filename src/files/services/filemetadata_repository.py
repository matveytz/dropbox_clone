from django.contrib.auth import get_user_model

from files.usecase.repository import AbstractRepository
from files.models import FileMetadata


class FileMetadataRepository(AbstractRepository[FileMetadata]):

    def create(self, **kwargs) -> FileMetadata:
        """
        Если нет kwargs, создается обьект по умолчанию
        """
        if not kwargs:
            kwargs = {
                "owner": get_user_model().objects.all().order_by('id').first(),
                "name": "default",
                "extension": "default",
                "size_bytes": 0,
                "hash_data": "default",
                "minio_key": "default",
                "other": [{}],
            }
        return FileMetadata.objects.create(**kwargs)

    def get_one(self, pk: str) -> FileMetadata:
        return FileMetadata.objects.filter(id=pk).get()

    def update_one(self, pk: str, **kwargs) -> FileMetadata:
        queryset = FileMetadata.objects.filter(id=pk)
        queryset.update(**kwargs)
        return queryset.get()


def filemetadata_repository_factory():
    return FileMetadataRepository()
