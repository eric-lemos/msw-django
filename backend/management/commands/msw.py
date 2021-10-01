from django.core.management.base import BaseCommand, CommandError
from backend.receivers.sennheiser.em6000 import em6000

class Command(BaseCommand):

    def handle(self, *args, **options):
        test = em6000(1, "192.168.0.5", 6970, "em6000", "PL70-EM6000")