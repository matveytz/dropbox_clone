import pytest

from django.contrib.auth import get_user_model

from files.models import FileMetadata
from .utils import _drop_database

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from django.contrib.auth.models import User


# INITIAL

#

# Database
@pytest.fixture(scope='session')
def django_db_modify_db_settings(django_db_modify_db_settings):
    from django.conf import settings

    settings.DATABASES['default']['USER'] = 'testuser'
    settings.DATABASES['default']['PASSWORD'] = 'postgresmaster'
    settings.DATABASES['default']['HOST'] = 'localhost'
    settings.DATABASES['default']['PORT'] = 5432


@pytest.fixture(scope='session')
def django_db_setup(
    request,
    django_db_blocker,
    superuser_schema,
    django_db_modify_db_settings,
    user_schema,
    filemetadata_schema,
):
    """Override top level fixture to ensure test databases are available"""
    from django.test.utils import setup_databases
    from django.conf import settings

    setup_databases_args = {}

    with django_db_blocker.unblock():

        # drop old test database
        _drop_database(**settings.DATABASES['default'])

        # setup and migrate
        setup_databases(
            verbosity=request.config.option.verbose,
            interactive=False,
            **setup_databases_args,
        )

        # load data
        get_user_model().objects.create_superuser(**superuser_schema)
        user = get_user_model().objects.create_user(**user_schema)
        FileMetadata.objects.create(owner=user, **filemetadata_schema)
    yield


# SCHEMAS

# User
@pytest.fixture(scope='session')
def superuser_schema() -> dict[str, Any]:
    return dict(
        username='test_superuser',
        email='test_superuser@mail.com',
        password='test_superuserpassword',
        is_staff=True,
        is_active=True,
        is_superuser=True,
    )


@pytest.fixture(scope='session')
def user_schema() -> dict[str, Any]:
    return dict(
        username='test_user',
        email='test_user@mail.com',
        password='test_userpassword',
        is_staff=False,
        is_active=True,
        is_superuser=False,
    )


# FileMetadata
@pytest.fixture(scope='session')
def default_filemetadata_schema() -> dict[str, Any]:
    return dict(
        name='default',
        extension='default',
        size_bytes=0,
        hash_data='default',
        minio_key='default',
        other=[{}],
    )


@pytest.fixture(scope='session')
def filemetadata_schema() -> dict[str, Any]:
    return dict(
        name='Photo',
        extension='.jpg',
        size_bytes=68900,
        hash_data='fake_hash',
        minio_key='fake_minio_key',
        other=[{'other': 'other'}],
    )


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
