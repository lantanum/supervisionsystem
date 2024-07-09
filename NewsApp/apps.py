from django.apps import AppConfig

class NewsappConfig(AppConfig):
    name = 'NewsApp'

    def ready(self):
        import NewsApp.signals
