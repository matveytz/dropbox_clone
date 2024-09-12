import pytest

from django.core.exceptions import ObjectDoesNotExist

from files.services.filemetadata_repository import FileMetadataRepository, FileMetadataStatusEnum

from uuid import UUID, uuid4


class TestFilemetadataRepository:

    @pytest.mark.django_db
    def test__create__none_kwargs(self, default_filemetadata_schema, superuser):
        repo = FileMetadataRepository()
        instance = repo.create()
        assert isinstance(instance.pk, UUID)
        assert instance.owner == superuser
        for attribute_name in default_filemetadata_schema:
            assert instance.__getattribute__(attribute_name) == default_filemetadata_schema[attribute_name]
        instance.delete()

    @pytest.mark.django_db
    def test__create(self, filemetadata_schema, user):
        repo = FileMetadataRepository()
        instance = repo.create(owner=user, **filemetadata_schema)
        assert isinstance(instance.pk, UUID)
        assert instance.owner == user
        for attribute_name in filemetadata_schema:
            assert instance.__getattribute__(attribute_name) == filemetadata_schema[attribute_name]
        instance.delete()

    @pytest.mark.django_db
    def test__get_one__bad_pk(self):
        repo = FileMetadataRepository()
        with pytest.raises(ObjectDoesNotExist):
            repo.get_one(str(uuid4()))

    @pytest.mark.django_db
    def test__get_one(self, filemetadata_schema, user):
        repo = FileMetadataRepository()
        instance = repo.create(owner=user, **filemetadata_schema)
        received_instance = repo.get_one(instance.pk)
        assert isinstance(received_instance.pk, UUID)
        assert received_instance.owner == user
        for attribute_name in filemetadata_schema:
            assert instance.__getattribute__(attribute_name) == filemetadata_schema[attribute_name]
        instance.delete()

    @pytest.mark.django_db
    def test__update_one__bad_pk(self):
        repo = FileMetadataRepository()
        with pytest.raises(ObjectDoesNotExist):
            repo.update_one(pk=str(uuid4()))

    @pytest.mark.django_db
    def test__update_one(self, default_filemetadata_schema, filemetadata_schema, user):
        repo = FileMetadataRepository()
        instance = repo.create(owner=user, **default_filemetadata_schema)
        received_instance = repo.update_one(pk=instance.pk, **filemetadata_schema)
        assert isinstance(received_instance.pk, UUID)
        assert received_instance.owner == user
        for attribute_name in filemetadata_schema:
            assert received_instance.__getattribute__(attribute_name) == filemetadata_schema[attribute_name]
        instance.delete()

    @pytest.mark.django_db
    def test__update_one__empty_kwargs(self, default_filemetadata_schema, user):
        repo = FileMetadataRepository()
        instance = repo.create(owner=user, **default_filemetadata_schema)
        received_instance = repo.update_one(pk=instance.pk)
        assert isinstance(received_instance.pk, UUID)
        assert received_instance.owner == user
        for attribute_name in default_filemetadata_schema:
            assert received_instance.__getattribute__(attribute_name) == default_filemetadata_schema[attribute_name]
        instance.delete()

    @pytest.mark.django_db
    def test__update_one__update_status(self, default_filemetadata_schema, user):
        repo = FileMetadataRepository()
        instance = repo.create(owner=user, **default_filemetadata_schema)
        received_instance = repo.update_one(pk=instance.pk, status=FileMetadataStatusEnum.on_error)
        assert isinstance(received_instance.pk, UUID)
        assert received_instance.status.title == FileMetadataStatusEnum.on_error.name
        assert received_instance.status.description == FileMetadataStatusEnum.on_error.value
        instance.delete()
