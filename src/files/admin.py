from django.contrib import admin

from .models import FileMetadata


@admin.register(FileMetadata)
class FileMetadataQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'name',
        'extension',
        'size_bytes',
        'last_used',
        'minio_key',
        'other',
        'created_at',
        'updated_at',
        'hash_data',
    )
