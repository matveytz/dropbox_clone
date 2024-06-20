from django.contrib.auth.models import User
from rest_framework import serializers

from .models import FileMetadata, FileMetadataStatus


class FileMetadataStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileMetadataStatus


class FileMetadataSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def update(self, instance, validated_data):
        print("update")
        return super().update(instance, validated_data)

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
            'status',
        )
        read_only_fields = (
            'id',
            'owner',
            'size_bytes',
            'last_used',
            'minio_key',
            'created_at',
            'updated_at',
            'hash_data',
            'status',
        )
