import pytest  # noqa: F401

from pytest_django.live_server_helper import LiveServer
from django.test import Client


class TestViews:
    def _(self, custom_client: Client, live_server: LiveServer):
        path = live_server.url + 'api/v1/files/'
        response = custom_client.get(path)
        assert response.status_code == 200
