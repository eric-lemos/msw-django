from flask import Flask, Response, request
from flask_restful import Resource, Api
from configs.settings import API_ROUTES
from backend.gateway import Gateway
from backend.views import views
from waitress import serve
from time import sleep

#========================= INSTANCES ==================#
wsgi_app = Flask(__name__)
streaming = Api(wsgi_app)
gateway = Gateway()

#========================= OVERVIEW ===================#
class overview(Resource):
    def get(self):
        def event():
            while(True):
                sleep(0.2)
                yield(f"data: {gateway.getOverview()} \n\n")
        return Response(event(), mimetype="text/event-stream")

#========================= AUDIT ======================#
class audit(Resource):
    def get(self):
        args = request.args.getlist("m")
        def event():
            while(True):
                sleep(0.2)
                yield(f"data: {gateway.getAudit(args)} \n\n")
        return Response(event(), mimetype="text/event-stream")

    def post(self):
        return gateway.postAudit(request.get_json())

#========================= REST =======================#
class zabbix(Resource):
    def get(self, id):
        return gateway.getZabbix(id)

#========================= ENDPOINTS ==================#
streaming.add_resource(audit, API_ROUTES["audit"]["get"], API_ROUTES["audit"]["post"])
streaming.add_resource(overview, API_ROUTES["overview"]["get"])
streaming.add_resource(zabbix, API_ROUTES["zabbix"]["get"])

def MSWStartServer():
    try:
        views.server.started()
        serve(wsgi_app, listen="*:5000", threads=12)
    except (KeyboardInterrupt): views.server.keyInterrupt()
    except Exception as e: views.server.exceptions(e)