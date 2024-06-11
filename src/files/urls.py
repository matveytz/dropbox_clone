# from django.urls import path, re_path
from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register(r'files', views.FileMetadataViewSet)
