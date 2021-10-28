from flask import Flask, Response, request
from flask_restful import Resource, Api
from configs.settings import ENDPOINTS
from backend.gateway import Gateway
from backend.monitor import Monitor
from backend.views import views
from waitress import serve
from time import sleep

#========================= MSW SERVER =================#
wsgi_app_1 = Flask(__name__)
wsgi_api_1 = Api(wsgi_app_1)
data_app_1 = Gateway()

class overview(Resource):
    def get(self):
        def event():
            while(True):
                sleep(0.2)
                yield(f"data: {data_app_1.getOverview()} \n\n")
        return Response(event(), mimetype="text/event-stream")

class audit(Resource):
    def get(self):
        args = request.args.getlist("m")
        def event():
            while(True):
                sleep(0.2)
                yield(f"data: {data_app_1.getAudit(args)} \n\n")
        return Response(event(), mimetype="text/event-stream")

    def post(self):
        return data_app_1.postAudit(request.get_json())

class zabbix(Resource):
    def get(self, id):
        return data_app_1.getZabbix(id)

class uptime(Resource):
    def get(self):
        return data_app_1.report()

wsgi_api_1.add_resource(overview, ENDPOINTS["get"]["overview"])
wsgi_api_1.add_resource(audit, ENDPOINTS["get"]["audit"], ENDPOINTS["post"]["audit"])
wsgi_api_1.add_resource(zabbix, ENDPOINTS["get"]["zabbix"])
wsgi_api_1.add_resource(uptime, "/")

def MSWStartServer():
    try:
        views.server.started("MSWStartServer", 5000)
        serve(wsgi_app_1, listen="*:5000", threads=12)
    except (KeyboardInterrupt): views.server.keyInterrupt("MSWStartServer")
    except Exception as e: views.server.exceptions("MSWStartServer", e)

#========================= MONITOR SERVER =============#
wsgi_app_2 = Flask(__name__)
wsgi_api_2 = Api(wsgi_app_2)
data_app_2 = Monitor()

class monitor(Resource):
    def get(self):
        return data_app_2.report()

wsgi_api_2.add_resource(monitor, "/")

def MonitorServer():
        try:
            views.server.started("MonitorServer", 5001)
            serve(wsgi_app_2, listen="*:5001")
        except (KeyboardInterrupt): views.server.keyInterrupt("MonitorServer")
        except Exception as e: views.server.exceptions("MonitorServer", e)