from configs.settings import TRANSMITTER_TIME, SUBSCRIBE_TIME
from backend.receivers.shure._ping import Shure
from backend.events import Device, Receive
from backend.models import Mics, Models
from backend.views import views
from threading import Thread
from time import time, sleep

class ur4d(Shure):
    def __init__(self, id, host, port, model, alias):
        super().__init__(host, port)
        self.answer_addr = (self.host, 27625)
        self.init(id, model, alias)
        self.threads()
    
    def init(self, id, model, alias):
        self.dev = Device()
        self.rx1 = Receive(self.dev)
        self.rx2 = Receive(self.dev)
        self.dev.host = self.host
        self.dev.port = self.port
        self.dev.model = model
        self.dev.alias = alias
        self.dev.id = id
        self.params()
        self.mics()

    def params(self):
        params = Models.objects.order_by("id").filter(model=self.dev.model)

        if(params):
            for param in params:
                self.dev.max_audio = param.max_aud
                self.dev.min_audio = param.min_aud
                self.dev.max_gain = param.max_gain
                self.dev.min_gain = param.min_gain
                self.dev.max_rf = param.max_rf
                self.dev.min_rf = param.min_rf

    def mics(self):
        mics_query = Mics.objects.order_by("id").filter(device_id=self.dev.id)

        if(not mics_query):
            Mics(name="mic001", detail="rx1", device_id=self.dev.id).save()
            Mics(name="mic002", detail="rx2", device_id=self.dev.id).save()
            mics_query = Mics.objects.order_by("id").filter(device_id=self.dev.id)

        if(mics_query):
            for mic in mics_query:
                if(mic.detail == "rx1"):
                    if(mic.alias): self.rx1.alias = mic.alias
                    self.rx1.detail = mic.detail
                    self.rx1.name = mic.name
                    self.rx1.id = mic.id
                    
                elif(mic.detail == "rx2"):
                    if(mic.alias): self.rx2.alias = mic.alias
                    self.rx2.detail = mic.detail
                    self.rx2.name = mic.name
                    self.rx2.id = mic.id
    
    def threads(self):
        Thread(target=self.ping).start()
        Thread(target=self.metering).start()
        Thread(target=self.receiver).start()

    #========================= OVERVIEW ===================#
    def getOverview(self):
        return {
            "device": self.dev.overview(),
            "receivers": {
                "rx1": self.rx1.overview(), 
                "rx2": self.rx2.overview()
            }
        }

    #========================= AUDIT ======================#
    def getAudit(self, device, mic):
        if((device == self.dev.id) and (mic == self.rx1.id)):
            return {
                "device": self.dev.audit(),
                "mic": self.rx1.audit()
            }
        elif((device == self.dev.id) and (mic == self.rx2.id)):
            return {
                "device": self.dev.audit(),
                "mic": self.rx2.audit()
            }

    def postAudit(self, mic, command, value):
        value = int(value)
        
        if(command == "gain"):
            if((value >= self.dev.min_gain) and (value <= self.dev.max_gain)):
                if(mic == self.rx1.id): self.post(f"* SET 1 AUDIO_GAIN {value} *")
                elif(mic == self.rx2.id): self.post(f"* SET 2 AUDIO_GAIN {value} *")
            else: return {"status": "error", "desc": views.audit.out_range(self.dev.model)}

        #elif(command == "n"): pass
        return {"status": "success"}

    #========================= ZABBIX =====================#
    def getZabbix(self, device, request_id):
        if((device == self.dev.id) and (request_id == self.rx1.id)): return self.rx1.zabbix(self.dev.ping)
        elif((device == self.dev.id) and (request_id == self.rx2.id)): return self.rx2.zabbix(self.dev.ping)

    #========================= SENDERS ====================#
    def metering(self):
        while(self.running):
            if(self.ping_state == "connected"):
                self.send('* METER 1 ALL 005 *')
                self.send('* METER 2 ALL 005 *')
                sleep(TRANSMITTER_TIME)
    
    #========================= RECEIVE ====================#
    @staticmethod
    def dBFS(value): return (((int(value)+1)/2)-128)

    @staticmethod
    def dBm(value): return ((int(value)-255)/2)

    @staticmethod
    def checkDiv(value):
        if(value == "AX"): return [1, 0]
        elif(value == "XB"): return [0, 1]
        elif(value == "AB"): return [1, 1]
        else: return [0, 0]

    @staticmethod
    def checkMute(data):
        if("OFF" in data): return False
        else: return True

    @staticmethod
    def isOnline(value):
        if("U" in value): return False
        else: return True

    def receiver(self):
        while(self.running):

            try: data, addr = self.read()
            except: data, addr = [0, 0]

            if((addr == self.answer_addr) and (data != 0)):
                data = data.split()

                #----------------------------- CAPSULE ------------------------#
                if("TX_TYPE" in data[3]): # Check if have ping updates #
                    self.recv_ping = time()
                    self.checkDeltaState()
                    self.dev.ping = self.ping_state

                    if("1" in data[2]):
                        self.rx1.capsule = data[4]

                    elif("2" in data[2]):
                        self.rx2.capsule = data[4]

                #----------------------------- METERING -----------------------#
                elif("ALL" in data[3]):
                    div = self.checkDiv(data[4])
                    if("1" in data[2]):
                        self.rx1.dva = div[0]
                        self.rx1.dvb = div[1]
                        self.rx1.rfa = self.dBm(data[5])
                        self.rx1.rfb = self.dBm(data[6])
                        self.rx1.audio = self.dBFS(data[8])
                        self.rx1.is_online = self.isOnline(data[7])
                        self.rx1.battery = data[7]

                    elif("2" in data[2]):
                        self.rx2.dva = div[0]
                        self.rx2.dvb = div[1]
                        self.rx2.rfa = self.dBm(data[5])
                        self.rx2.rfb = self.dBm(data[6])
                        self.rx2.audio = self.dBFS(data[8])
                        self.rx2.is_online = self.isOnline(data[7])
                        self.rx2.battery = data[7]
                    
                #----------------------------- NAME ---------------------------#
                elif("CHAN_NAME" in data[3]):
                    if("1" in data[2]):
                        self.rx1.alias = str(data[4])

                    elif("2" in data[2]):
                        self.rx2.alias = str(data[4])

                #----------------------------- GAIN ---------------------------#
                elif("AUDIO_GAIN" in data[3]):
                    if("1" in data[2]):
                        self.rx1.gain = int(data[4])

                    elif("2" in data[2]):
                        self.rx2.gain = int(data[4])
                
                #----------------------------- MUTE ---------------------------#
                elif("MUTE" in data[3]):
                    if("1" in data[2]):
                        self.rx1.mute = self.checkMute(str(data[4]))

                    elif("2" in data[2]):
                        self.rx2.mute = self.checkMute(str(data[4]))
                
                #----------------------------- GROUP --------------------------#
                elif("GROUP_CHAN" in data[3]):
                    if("1" in data[2]):
                        self.rx1.group = (int(data[4]), int(data[5]))

                    elif("2" in data[2]):
                        self.rx2.group = (int(data[4]), int(data[5]))
                
                #----------------------------- FREQ ---------------------------#
                elif("FREQUENCY" in data[3]):
                    if("1" in data[2]):
                        self.rx1.carrier = int(data[4])

                    elif("2" in data[2]):
                        self.rx2.carrier = int(data[4])