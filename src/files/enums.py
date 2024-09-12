from enum import Enum


class FileMetadataStatusEnum(Enum):
    """
    Перечисления для статуса FileMetadata
    формат: title = description
    """
    untracked = 'File not tracked on storage backend'
    loaded = 'File load and exsist on storage backend'
    deleted = 'File exsist, but not tracked on storage backend'
    on_error = 'Some error with file (probably missing on storge backend)'
