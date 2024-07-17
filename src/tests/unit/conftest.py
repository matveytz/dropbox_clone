import pytest

from django.contrib.auth import get_user_model

from files.models import FileMetadata
from files.constants import DEFAULT_FILEMETADATA_SCHEMA

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from django.contrib.auth.models import User


# SCHEMAS

# Prepare
def _superuser_schema() -> dict[str, Any]:
    return dict(
        username='test_superuser',
        email='test_superuser@mail.com',
        password='test_superuserpassword',
        is_staff=True,
        is_active=True,
        is_superuser=True,
    )


def _user_schema() -> dict[str, Any]:
    return dict(
        username='test_user',
        email='test_user@mail.com',
        password='test_userpassword',
        is_staff=False,
        is_active=True,
        is_superuser=False,
    )


def _default_filemetadata_schema() -> dict[str, Any]:
    return DEFAULT_FILEMETADATA_SCHEMA.copy()


def _filemetadata_schema() -> dict[str, Any]:
    return dict(
        name='Photo',
        extension='.jpg',
        size_bytes=68900,
        hash_data='fake_hash',
        minio_key='fake_minio_key',
        other=[{'other': 'other'}],
    )


# User
@pytest.fixture
def superuser_schema() -> dict[str, Any]:
    return _superuser_schema()


@pytest.fixture
def user_schema() -> dict[str, Any]:
    return _user_schema()


@pytest.fixture(scope='session')
def superuser_schema_session() -> dict[str, Any]:
    return _superuser_schema()


@pytest.fixture(scope='session')
def user_schema_session() -> dict[str, Any]:
    return _user_schema()


# FileMetadata
@pytest.fixture
def default_filemetadata_schema() -> dict[str, Any]:
    return _default_filemetadata_schema()


@pytest.fixture
def filemetadata_schema() -> dict[str, Any]:
    return _filemetadata_schema()


@pytest.fixture(scope='session')
def filemetadata_schema_session() -> dict[str, Any]:
    return _filemetadata_schema()


# GETTERS

# User instance
@pytest.fixture
def superuser(db, superuser_schema):
    return get_user_model().objects.filter(
        username=superuser_schema['username'],
    ).get()


@pytest.fixture
def user(db, user_schema):
    return get_user_model().objects.filter(
        username=user_schema['username'],
    ).get()


# FileMetadata instance
@pytest.fixture
def default_filemetadata(db, default_filemetadata_schema, user: "User") -> FileMetadata:
    return FileMetadata.objects.filter(
        owner=user,
        **default_filemetadata_schema,
    ).get()


@pytest.fixture
def filemetadata(db, filemetadata_schema, user: "User") -> FileMetadata:
    return FileMetadata.objects.filter(
        owner=user,
        **filemetadata_schema,
    ).get()
