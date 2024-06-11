from rest_framework import viewsets, mixins

from .models import FileMetadata
from .serializer import FileMetadataSerializer


class ListRetrieveUpdateDestroyFileMetadataViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = FileMetadata.objects.all()
    serializer_class = FileMetadataSerializer
    permission_classes = []


class DownloadFileMetadataViewSet(
    viewsets.ViewSet
):
    def download(self, request, pk=None):
        pass


class UploadFileMetadataViewSet(
    viewsets.ViewSet
):
    def upload(self, request, pk=None):
        pass
