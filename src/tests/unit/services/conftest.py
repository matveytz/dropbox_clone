import pytest

from typing import Any


# SCHEMAS

# Prepare
def _post_webhook_schema() -> dict[str, Any]:
    return {
        'api': {
            'statusCode': 200,
            'name': 'PostPolicyBucket',
            'bucket': 'test_bucket',
        },
        'tags': {
            'objectLocation': {
                'name': 'filename.extension',
            },
        },
        'responseHeader': {
            'ETag': 'test_etag',
        },
    }


# Webhook data
@pytest.fixture
def post_webhook_schema() -> dict[str, Any]:
    return _post_webhook_schema()


# MOCK

# Repository
@pytest.fixture
def mock_repository():
    from files.usecase.repository import AbstractRepository

    class MockRepository(AbstractRepository):
        def __init__(self) -> None:
            self.data = {}

        def create(self, **kwargs) -> Any:
            self.data[kwargs.pop('pk')] = kwargs

        def get_one(self, pk: str) -> Any:
            return self.data[pk]

        def update_one(self, pk: str, **kwargs) -> Any:
            self.data[pk] = kwargs
            return self.data[pk]

    return MockRepository()


# S3
@pytest.fixture
def mock_s3():
    from files.usecase.s3 import AbstractS3

    FAKE_FILESIZE = 10

    class MockS3(AbstractS3):
        def get_upload_policy(
            self,
            new_bucket: str,
        ) -> dict[str, str]:
            return {
                'new_bucket': new_bucket,
            }

        def get_file_download_url(
            self,
            file_id: str,
            filename: str,
        ) -> str | None:
            return f'{file_id=}; {filename=}'

        def get_file_size(self, filename: str, bucket: str) -> int | None:
            return FAKE_FILESIZE

    return MockS3()
