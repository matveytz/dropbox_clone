from django.urls import path
from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register(r'files', views.FileMetadataViewSet)

urlpatterns = [
    path('minio-webhook/', views.MinIOWebhookView.as_view(), name='minio_webhook'),
]
urlpatterns += router.urls
