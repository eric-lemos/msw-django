from django.core.management.base import BaseCommand, CommandError
from backend.stream import MSWStartServer
from backend.gateway import Gateway
from backend.stream import wsgi_app
from backend.views import views

class Command(BaseCommand):

    def handle(self, *args, **options):
        MSWStartServer()