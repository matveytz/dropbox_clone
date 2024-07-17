import pytest

from django.test import Client


@pytest.fixture
def custom_client(client: Client):
    return client
