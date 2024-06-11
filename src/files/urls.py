from django.urls import path

from . import views


file_metadata_detail = views.ListRetrieveUpdateDestroyFileMetadataViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})
file_metadata_list = views.ListRetrieveUpdateDestroyFileMetadataViewSet.as_view({
    'get': 'list',
})
file_metadata_download = views.DownloadFileMetadataViewSet.as_view({
    'get': 'download',
})
file_metadata_upload = views.UploadFileMetadataViewSet.as_view({
    'post': 'upload',
})

urlpatterns = [
    path('files/', file_metadata_list, name='file_metadata_list'),
    path('files/<uuid:pk>/', file_metadata_detail, name='file_metadata_detail'),
    path('files/<uuid:pk>/download', file_metadata_download, name='file_metadata_download'),
    path('files/<uuid:pk>/upload', file_metadata_upload, name='file_metadata_upload'),
]
