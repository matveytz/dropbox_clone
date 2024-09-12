# Generated by Matvey Baranov on 2024-07-10 15:25

from django.db import migrations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from django.db.migrations.state import StateApps
    from django.db.backends.postgresql.schema import DatabaseSchemaEditor

from files.enums import FileMetadataStatusEnum


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial')
    ]

    @staticmethod
    def insertData(apps: "StateApps", schema_editor: "DatabaseSchemaEditor"):
        filemetadata_status = apps.get_model('files', 'FileMetadataStatus')
        for status in FileMetadataStatusEnum:
            result, created = filemetadata_status.objects.get_or_create(
                title=status.name,
                defaults=dict(description=status.value),
            )

    operations = [
        migrations.RunPython(insertData),
    ]
