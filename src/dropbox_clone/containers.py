from dependency_injector import containers, providers

from files.services import MinIOService, MinIOWebhookService, FileMetadataRepository

from . import settings


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(ini_files=["config.ini"])

    s3_service = providers.Factory(
        MinIOService,
        endpoint=config.MINIO_ENDPOINT,
        access_key=config.MINIO_ACCES_KEY,
        secret_key=config.MINIO_SECRET_KEY,
    )

    webhook_service = providers.Factory(
        MinIOWebhookService,
    )

    filemetadata_repository = providers.Factory(
        FileMetadataRepository
    )


container = Container()
container.config.from_dict(settings.__dict__)
