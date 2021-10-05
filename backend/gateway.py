from backend.receivers.sennheiser.em6000 import em6000
from backend.receivers.shure.ur4d import ur4d
from django.db.models import Count
from backend.models import Devices, Mics
from backend.views import views
from json import dumps

class Gateway:
    def __init__(self):
        self.devices = Devices.objects.all()
        self.objects = {}
        self.load()

    def load(self):
        for device in self.devices:
            if(str(device.model) == "em6000"):
                self.objects[device.id] = em6000(device.id, device.host, device.port, str(device.model), device.alias)

            # elif(str(device.model) == "ur4d"):
                # self.objects[device.id] = ur4d(device.id, device.host, device.port, str(device.model), device.alias)

    #========================= OVERVIEW ===================#
    def getOverview(self):
        results = []
        for device in self.devices:
            if(self.objects[device.id] is not None):
                results.append(self.objects[device.id].getOverview())
        return dumps(results)
         
    #========================= AUDIT ======================#
    def getAudit(self, args):
        results = []
        for device in self.devices:
            if(self.objects[device.id] is not None):
                for mics in Mics.objects.filter(device=device.id):
                    for mic in args:
                        mic = int(mic)
                        if(mic == mics.id):
                            if(mic not in results):
                                results.append(self.objects[device.id].getAudit(device.id, mic))
        return dumps(results)

    @staticmethod
    def checkPost(data, keys):
        if(data is not None):
            numKeys = len(keys)
            for i in range(numKeys):
                if(keys[i] not in data):
                    return {"status": "error"}
            return {"status": "success"}
        else: return {"status": "error"}

    def postAudit(self, data):
        keys = ["id", "mic", "cmd", "value"]
        result = self.checkPost(data, keys)

        if(result["status"] == "success"):
            for device in self.devices:
                if(self.objects[device.id] is not None):
                    if(data["id"] == self.objects[device.id].dev.id):
                        return self.objects[device.id].postAudit(data["mic"], data["cmd"], data["value"])
                    else: return {"status": "error", "desc": views.audit.null_object()}
                else: return {"status": "error", "desc": views.audit.not_exist()}

    #========================= ZABBIX =====================#
    def getZabbix(self, request_id):
        for device in self.devices:
            if(self.objects[device.id] is not None):
                result = self.objects[device.id].getZabbix(device.id, request_id)
                if(result is not None): return result