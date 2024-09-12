from django.contrib.auth.models import User
from rest_framework import serializers

from .models import FileMetadata, FileMetadataStatus


class FileMetadataStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileMetadataStatus


class FileMetadataSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    status = serializers.SlugRelatedField(read_only=True, slug_field='title')

    class Meta:
        model = FileMetadata
        fields = (
            'id',
            'owner',
            'name',
            'extension',
            'size_bytes',
            'minio_key',
            'created_at',
            'updated_at',
            'other',
            'hash_data',
            'status',
        )
        read_only_fields = (
            'id',
            'owner',
            'size_bytes',
            'minio_key',
            'created_at',
            'updated_at',
            'hash_data',
            'status',
        )
