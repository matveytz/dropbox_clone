from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from dependency_injector.wiring import inject, Provide

from dropbox_clone.containers import Container
from .models import FileMetadata
from .serializer import FileMetadataSerializer
from .usecase import s3, webhook_hendler
from .utils import FileMetadataStatusEnum

from logging import getLogger
from datetime import datetime, timezone
import json


logger = getLogger(__name__)


class FileMetadataViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = FileMetadata.objects.all()
    serializer_class = FileMetadataSerializer

    def destroy(self, request, *args, **kwargs):
        instance: FileMetadata = self.get_object()
        instance.update_status(FileMetadataStatusEnum.deleted)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @inject
    @action(methods=['get'], detail=True, permission_classes=())
    def download_url(
        self,
        request,
        pk=None,
        s3_service: s3.AbstractS3Service = Provide[Container.s3_service],
    ):
        url = s3_service.get_file_download_url(str(pk))
        if url is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        FileMetadata.objects.filter(id=pk).update(last_used=datetime.now(timezone.utc))
        return Response(data={'url': url}, status=status.HTTP_200_OK)

    @inject
    @action(methods=['get'], detail=False, permission_classes=())
    def upload_url(
        self,
        request,
        s3_service: s3.AbstractS3Service = Provide[Container.s3_service],
    ):
        form_data = s3_service.get_upload_policy()
        return Response(data=form_data, status=status.HTTP_201_CREATED)


class MinIOWebhookView(APIView):

    def post(
        self,
        request,
        s3_webhook_service: webhook_hendler.WebhookHandler = Provide[Container.webhook_service]
    ):
        webhook_data = request.data
        logger.info(json.dumps(webhook_data))
        s3_webhook_service.webhook_handler_template(webhook_data)
        return Response(data=webhook_data, status=status.HTTP_200_OK)
