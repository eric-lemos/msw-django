from django.core.management.base import BaseCommand
from backend.stream import MSWStartServer

class Command(BaseCommand):

    def handle(self, *args, **options):
        MSWStartServer()