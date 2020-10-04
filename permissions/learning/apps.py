from django.apps import AppConfig


class LearningConfig(AppConfig):
    name = 'learning'

    def ready(self):
        try:
            import learning.signals  # noqa F401
        except ImportError:
            pass
