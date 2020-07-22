from django.apps import AppConfig


class DownloadConfig(AppConfig):
    name = 'download'

    def ready(self):
    	from Tasks import updater
    	updater.start()