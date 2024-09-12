import pytest  # noqa: F401

from files.usecase.webhook_handler import WebhookHandler
from files.services.s3_webhook_handler import MinIOWebhookService, FileMetadataStatusEnum

FAKE_RETURN = 'FAKE_RETURN'
FAKE_KEY = 'FAKE_KEY'
FAKE_DEFAULT_RETURN = 'FAKE_DEFAULT_RETURN'
FAKE_WEBHOOK_DATA = 'FAKE_WEBHOOK_DATA'


class TestUsecaseWebhookhandler:

    def test_none_key(self):
        class FakeWebhookHandler(WebhookHandler):

            def get_mapping_key(self, webhook_data) -> str | None:
                return None

            def default_handler(self, webhook_data):
                return (FAKE_DEFAULT_RETURN, webhook_data)

        webhook_handler = FakeWebhookHandler()
        res = webhook_handler.webhook_handler_template(FAKE_WEBHOOK_DATA)
        assert res == (FAKE_DEFAULT_RETURN, FAKE_WEBHOOK_DATA)

    def test_key_not_impemented_in_method_handle_mapping(self):
        class FakeWebhookHandler(WebhookHandler):

            def get_mapping_key(self, webhook_data) -> str | None:
                return FAKE_KEY

            def fake_handler(self, webhook_data):
                return (FAKE_RETURN, webhook_data)

            method_handle_mapping = {
                'NOT_IMPLEMENTED': fake_handler
            }

        webhook_handler = FakeWebhookHandler()
        with pytest.raises(NotImplementedError):
            webhook_handler.webhook_handler_template(FAKE_WEBHOOK_DATA)

    def test_key_impemented_in_method_handle_mapping(self):
        class FakeWebhookHandler(WebhookHandler):

            def get_mapping_key(self, webhook_data) -> str | None:
                return FAKE_KEY

            def fake_handler(self, webhook_data):
                return (FAKE_RETURN, webhook_data)

            method_handle_mapping = {
                FAKE_KEY: fake_handler
            }

        webhook_handler = FakeWebhookHandler()
        res = webhook_handler.webhook_handler_template(FAKE_WEBHOOK_DATA)
        assert res == (FAKE_RETURN, FAKE_WEBHOOK_DATA)


class TestS3WebhookHandler:
    def test__get_mapping_key__webhook_data__invalid(self):
        webhook_service = MinIOWebhookService()
        with pytest.raises(KeyError):
            webhook_service.get_mapping_key(webhook_data={})

    def test__get_mapping_key__webhook_data__status_code__not_equal_200(self, post_webhook_schema):
        webhook_service = MinIOWebhookService()
        post_webhook_schema['api']['statusCode'] = 400

        key = webhook_service.get_mapping_key(webhook_data=post_webhook_schema)

        assert key is None

    def test__get_mapping_key__webhook_data__valid(self, post_webhook_schema):
        webhook_service = MinIOWebhookService()

        key = webhook_service.get_mapping_key(webhook_data=post_webhook_schema)

        assert key == 'PostPolicyBucket'

    def test__post_policy_bucket_handler__webhook_data__invalid(self):
        webhook_service = MinIOWebhookService()
        with pytest.raises(KeyError):
            webhook_service.post_policy_bucket_handler(webhook_data={})

    def test__post_policy_bucket_handler__valid(
        self,
        post_webhook_schema,
        mock_repository,
        mock_s3,
    ):
        webhook_service = MinIOWebhookService()
        mock_repository.create(pk=post_webhook_schema['api']['bucket'])
        webhook_service.post_policy_bucket_handler(post_webhook_schema, mock_repository, mock_s3)
        repository_state = mock_repository.data.popitem()
        assert repository_state[0] == post_webhook_schema['api']['bucket']
        repository_state = repository_state[1]
        assert repository_state['name'] + repository_state['extension'] == post_webhook_schema['tags']['objectLocation']['name']  # noqa: E501
        assert repository_state['size_bytes'] == 10
        assert repository_state['hash_data'] == post_webhook_schema['responseHeader']['ETag']
        assert repository_state['minio_key'] == f"{post_webhook_schema['api']['bucket']}/{post_webhook_schema['tags']['objectLocation']['name']}"  # noqa: E501
        assert repository_state['status'] == FileMetadataStatusEnum.loaded
