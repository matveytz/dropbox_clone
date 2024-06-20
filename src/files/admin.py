from django.contrib import admin

from .models import FileMetadata, FileMetadataStatus


@admin.register(FileMetadata)
class FileMetadataAdmin(admin.ModelAdmin):
    list_display = (
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


@admin.register(FileMetadataStatus)
class FileMetadataStatusAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'description',
    )
