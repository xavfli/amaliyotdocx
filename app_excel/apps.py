from django.apps import AppConfig

class AppExcelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_excel'

    def ready(self):
        import app_excel.signals

