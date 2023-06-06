import time
from base_apps.game_server.models import Server
from base_apps.game_server_config.models import Config
from management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        Config.objects.exclude(
            server_id__in=Server.objects.values_list('id',flat=True)
        ).delete()
        while True:
            self.call_command('server_config_worker_loop')
            time.sleep(1)

