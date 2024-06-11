from django.contrib.auth.models import User
from rest_framework import serializers

from .models import FileMetadata


class FileMetadataSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = FileMetadata
        fields = (
            'id',
            'owner',
            'name',
            'extension',
            'size_bytes',
            'last_used',
            'minio_key',
            'created_at',
            'updated_at',
            'other',
            'hash_data',
        )
