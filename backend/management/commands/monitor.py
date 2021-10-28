from django.core.management.base import BaseCommand
from flask_restful import Resource, Api
from backend.monitor import Monitor
from backend.views import views
from waitress import serve
from flask import Flask

class Command(BaseCommand):

    def handle(self, *args, **options):

        wsgi_app = Flask(__name__)
        wsgi_api = Api(wsgi_app)
        _monitor = Monitor()

        class monitor(Resource):
            def get(self):
                return _monitor.report()
        
        wsgi_api.add_resource(monitor, "/")

        try:
            views.server.started("MonitorCommand", 5001)
            serve(wsgi_app, listen="*:5001")
        except (KeyboardInterrupt): views.server.keyInterrupt("MonitorCommand")
        except Exception as e: views.server.exceptions("MonitorCommand", e)