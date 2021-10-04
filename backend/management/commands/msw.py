from django.core.management.base import BaseCommand, CommandError
from backend.gateway import Gateway
from backend.stream import wsgi_app
from backend.views import views
from waitress import serve

class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            views.server.started()
            serve(wsgi_app, listen="*:5000", threads=12)
        except (KeyboardInterrupt): views.server.keyInterrupt()
        except Exception as e: views.server.exceptions(e)

        #========================= TESTS ==================#
        #g = Gateway()