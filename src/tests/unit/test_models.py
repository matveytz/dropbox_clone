import pytest # noqa: F401, E261

from files.models import FileMetadata, FileMetadataStatus
from files.enums import FileMetadataStatusEnum
from files.constants import DEFAULT_FILEMETADATA_STATUS

from uuid import UUID

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from django.contrib.auth.models import User


class TestUser:

    def test_user_instance_equal_schema(self, user: "User", user_schema: dict[str, Any]):
        assert user.username == user_schema['username']
        assert user.email == user_schema['email']
        assert user.check_password(user_schema['password'])
        assert user.is_staff == user_schema['is_staff']
        assert user.is_active == user_schema['is_active']
        assert user.is_superuser == user_schema['is_superuser']

    def test_superuser_instance_equal_schema(self, superuser: "User", superuser_schema: dict[str, Any]):
        assert superuser.username == superuser_schema['username']
        assert superuser.email == superuser_schema['email']
        assert superuser.check_password(superuser_schema['password'])
        assert superuser.is_staff == superuser_schema['is_staff']
        assert superuser.is_active == superuser_schema['is_active']
        assert superuser.is_superuser == superuser_schema['is_superuser']

    def test_user_is_not_superuser(self, user: "User"):
        assert not user.is_superuser
        assert not user.is_staff

    def test_superuser_is_superuser(self, superuser: "User"):
        assert superuser.is_superuser
        assert superuser.is_staff

    def test_user_not_equal_superuser(self, user: "User", superuser: "User"):
        assert superuser.username != user.username
        assert superuser.email != user.email
        assert superuser.is_staff != user.is_staff
        assert superuser.is_superuser != user.is_superuser

    def test_user_and_superuser_active(self, user: "User", superuser: "User"):
        assert superuser.is_active and user.is_active


class TestFileMetadata:

    def test_filemetadata_pk_is_uuid(self, filemetadata: FileMetadata):
        assert isinstance(filemetadata.pk, UUID)

    def test_filemetadata_equal_schema(self, filemetadata: FileMetadata, filemetadata_schema):
        assert filemetadata.name == filemetadata_schema['name']
        assert filemetadata.extension == filemetadata_schema['extension']
        assert filemetadata.size_bytes == filemetadata_schema['size_bytes']
        assert filemetadata.hash_data == filemetadata_schema['hash_data']
        assert filemetadata.minio_key == filemetadata_schema['minio_key']
        assert filemetadata.other == filemetadata_schema['other']

    def test_filemetadata_not_equal_default_schema(self, filemetadata: FileMetadata, default_filemetadata_schema):
        assert filemetadata.name != default_filemetadata_schema['name']
        assert filemetadata.extension != default_filemetadata_schema['extension']
        assert filemetadata.size_bytes != default_filemetadata_schema['size_bytes']
        assert filemetadata.hash_data != default_filemetadata_schema['hash_data']
        assert filemetadata.minio_key != default_filemetadata_schema['minio_key']
        assert filemetadata.other != default_filemetadata_schema['other']

    def test_filemetadata_get_filename(self, filemetadata: FileMetadata, filemetadata_schema):
        filename = filemetadata.get_filename()
        filename_example = filemetadata_schema['name'] + filemetadata_schema['extension']

        assert filename == filename_example

    def test_filemetadata_update_status_not_change(self, filemetadata: FileMetadata):
        status_enum_instance = FileMetadataStatusEnum[filemetadata.status.title]
        old_status_pk = filemetadata.status.pk
        old_status_title = filemetadata.status.title

        FileMetadata.objects.update_status(id=filemetadata.pk, status=status_enum_instance)

        assert old_status_pk == filemetadata.status.pk
        assert old_status_title == filemetadata.status.title

    def test_filemetadata_update_status_changed(self, filemetadata: FileMetadata):
        status_enum_instance = FileMetadataStatusEnum[filemetadata.status.title]
        old_status_pk = filemetadata.status.pk
        old_status_title = filemetadata.status.title
        new_status = FileMetadataStatusEnum.deleted
        if new_status == status_enum_instance:
            new_status = FileMetadataStatusEnum.loaded

        new_filemetadata = FileMetadata.objects.update_status(id=filemetadata.pk, status=new_status).get()

        assert old_status_pk != new_filemetadata.status.pk
        assert old_status_title != new_filemetadata.status.title

    @pytest.mark.django_db
    def test_filemetadata_status_get_defult(self):
        status = FileMetadataStatus.objects.get_default_status()
        assert status.title == DEFAULT_FILEMETADATA_STATUS.name
        assert status.description == DEFAULT_FILEMETADATA_STATUS.value

    @pytest.mark.django_db
    def test_filemetadata_status_get_status(self):
        for instance in FileMetadataStatusEnum:
            status = FileMetadataStatus.objects.get_status(instance)
            assert status.title == instance.name
            assert status.description == instance.value
