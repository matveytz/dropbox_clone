from datetime import timedelta
from .enums import FileMetadataStatusEnum

DEFAULT_PART_SIZE = 5*1024*1024
DEFAULT_URL_EXPIRE = timedelta(hours=1)
DEFAULT_CONNECTION_TIMEOUT = timedelta(seconds=10).total_seconds()
MIN_FILE_SIZE = 10
MAX_FILE_SIZE = 512*1024*1024
MINIO_DEBAG_URL = 'http://localhost:9000'
DEFAULT_FILEMETADATA_STATUS = FileMetadataStatusEnum.untracked
DEFAULT_FILEMETADATA_SCHEMA = {
    "name": "default",
    "extension": "default",
    "size_bytes": 0,
    "hash_data": "default",
    "minio_key": "default",
    "other": [{}],
}
