# Generated by Django 5.0.6 on 2024-06-20 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_filemetadatastatus_alter_filemetadata_size_bytes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filemetadata',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]