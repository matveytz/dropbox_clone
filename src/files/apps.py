from django.apps import AppConfig


class FilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'files'

    def ready(self) -> None:
        from dropbox_clone.containers import container
        print("App ready")
        container.wire(modules=[".views"])
