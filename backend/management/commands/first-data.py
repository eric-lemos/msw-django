from django.core.management.base import BaseCommand
from django.core.management import call_command
import django
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        django.setup()
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
        call_command("loaddata", "configs", app="backend")
        call_command("loaddata", "models", app="backend")