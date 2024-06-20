from django.db import models
from django.contrib.auth import get_user_model

from enum import Enum
import uuid

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from django.contrib.auth.models import User


class BaseModel(models.Model):
    """
    Базовая модель для таблиц с первичным ключом типа UUID
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        abstract = True


class FileMetadataStatusEnum(Enum):
    """
    Перечисления для статуса FileMetadata
    формат: typle(title, description)
    """
    untracked = 'untracked', 'File not tracked on storage backend'
    loaded = 'loaded', 'File load and exsist on storage backend'
    deleted = 'deleted', 'File exsist, but not tracked on storage backend'
    on_error = 'on_error', 'Some error with file (probably missing on storge backend)'


def get_first_user_instance() -> "User":
    """
    Возвращает первого пользователя в таблице User.
    Используется пока не настроена авторизация, для коректной работы с владельцами Filemetadata (owner)
    """
    return get_user_model().objects.all().order_by('id').first()


def get_default_filemetadata():
    return {
        "owner": get_first_user_instance(),
        "name": "default",
        "extension": "default",
        "size_bytes": 0,
        "hash_data": "default",
        "minio_key": "default",
        "other": [{}],
    }
