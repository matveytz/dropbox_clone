import pytest

from django.contrib.auth import get_user_model

from files.models import FileMetadata
from tests.utils import _drop_database


# INITIAL

# Database
@pytest.fixture(scope='session')
def django_db_modify_db_settings():
    from django.conf import settings

    settings.DATABASES['default']['USER'] = 'testuser'
    settings.DATABASES['default']['PASSWORD'] = 'postgresmaster'
    settings.DATABASES['default']['HOST'] = 'localhost'
    settings.DATABASES['default']['PORT'] = 5432


@pytest.fixture(scope='session')
def django_db_setup(
    request,
    django_db_blocker,
    django_db_modify_db_settings,
    superuser_schema_session,
    user_schema_session,
    filemetadata_schema_session,
):
    """Override top level fixture to ensure test databases are available"""
    from django.test.utils import setup_databases
    from django.conf import settings

    setup_databases_args = {}

    with django_db_blocker.unblock():

        # drop old test database
        _drop_database(**(settings.DATABASES['default']))

        # setup and migrate
        setup_databases(
            verbosity=request.config.option.verbose,
            interactive=False,
            **setup_databases_args,
        )

        # load data
        get_user_model().objects.create_superuser(**superuser_schema_session)
        user = get_user_model().objects.create_user(**user_schema_session)
        FileMetadata.objects.create(owner=user, **filemetadata_schema_session)
    yield
