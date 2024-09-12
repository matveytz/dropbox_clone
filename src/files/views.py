from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from .models import FileMetadata, FileMetadataStatusEnum
from .serializer import FileMetadataSerializer
from .services.minio_facade import s3_factory
from .services.s3_webhook_handler import webhook_service_factory
from .services.filemetadata_repository import filemetadata_repository_factory

from logging import getLogger
import json
from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from .usecase.webhook_handler import WebhookHandler
    from .usecase.repository import AbstractRepository
    from .services.minio_facade import MinIOFacade

logger = getLogger(__name__)


class FileMetadataViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = FileMetadata.objects.all()
    serializer_class = FileMetadataSerializer
    repository_factory: "Callable[[], AbstractRepository]" = filemetadata_repository_factory
    s3_service_factory: "Callable[[], MinIOFacade]" = s3_factory

    def destroy(self, request, *args, **kwargs):
        instance: FileMetadata = self.get_object()
        instance.update_status(FileMetadataStatusEnum.deleted)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True, permission_classes=())
    def download_url(self, request, pk=None):
        repository = self.__class__.repository_factory()
        s3_service = self.__class__.s3_service_factory()
        pk = str(pk)
        instance: FileMetadata = repository.get_one(pk)
        url = s3_service.get_file_download_url(pk, instance.get_filename())
        if url is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'url': url}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, permission_classes=())
    def upload_url(self, request):
        repository = self.__class__.repository_factory()
        s3_service = self.__class__.s3_service_factory()
        instance: FileMetadata = repository.create()
        form_data = s3_service.get_upload_policy(str(instance.pk))
        return Response(data=form_data, status=status.HTTP_201_CREATED)


class MinIOWebhookView(APIView):
    service: "WebhookHandler" = webhook_service_factory()

    def post(self, request):
        webhook_data = request.data
        logger.info(json.dumps(webhook_data))
        self.service.webhook_handler_template(webhook_data)
        return Response(data=webhook_data, status=status.HTTP_200_OK)
