from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.decorators import action
from django.core.files.uploadedfile import UploadedFile

from .models import FileMetadata
from .serializer import FileMetadataSerializer
from .services import MinIOService


class FileMetadataViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = FileMetadata.objects.all()
    serializer_class = FileMetadataSerializer
    parser_classes = (FileUploadParser,)
    permission_classes = ()

    @action(methods=['get'], detail=True, permission_classes=())
    def download(self, request, pk=None):
        return Response(status=200)

    @action(methods=['post'], detail=False, permission_classes=())
    def upload(self, request):
        """Required:
        Content-Disposition: attachment; filename=upload.jpg
        """
        file_obj: UploadedFile = request.data['file']
        minio = MinIOService()
        minio.upload_file(file_obj.name, file_obj)
        return Response(status=204)
