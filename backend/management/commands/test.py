from django.core.management.base import BaseCommand, CommandError
from backend.receivers.sennheiser.em6000 import em6000
from backend.receivers.shure.ur4d import ur4d

class Command(BaseCommand):

    def handle(self, *args, **options):
        #sennheiser = em6000(1, "192.168.0.5", 6970, "em6000", "PL70-EM6000")
        shure = ur4d(2, "192.168.0.6", 2202, "ur4d", "PL70-CT-UR4D-A")