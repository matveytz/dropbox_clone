from django.db import models
from django.conf import settings

from .utils import BaseModel


class FileMetadata(BaseModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=256)
    extension = models.CharField(max_length=32)
    size_bytes = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_used = models.DateTimeField(auto_now_add=True)
    hash_data = models.CharField(max_length=256)
    minio_key = models.CharField()
    other = models.JSONField(default=list)
