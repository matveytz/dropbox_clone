from files.usecase.repository import AbstractRepository
from files.models import FileMetadata
from files.utils import get_default_filemetadata


class FileMetadataRepository(AbstractRepository[FileMetadata]):

    def create(self, **kwargs) -> FileMetadata:
        """
        Если нет kwargs, создается обьект по умолчанию
        """
        if not kwargs:
            kwargs = get_default_filemetadata()
        return FileMetadata.objects.create(**kwargs)

    def get_one(self, pk: str) -> FileMetadata:
        return FileMetadata.objects.filter(id=pk).get()

    def update_one(self, pk: str, **kwargs) -> FileMetadata:
        queryset = FileMetadata.objects.filter(id=pk)
        queryset.update(**kwargs)
        return queryset.get()


def filemetadata_repository_factory():
    return FileMetadataRepository()
