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
        #Thread(target=self.ping).start()
        # Thread(target=self.TxGain).start()
        # Thread(target=self.TxMute).start()
        # Thread(target=self.TxGroup).start()
        Thread(target=self.TxMetering).start()
        Thread(target=self.receiver).start()
        # Thread(target=self.TxBattery).start()
        # Thread(target=self.TxCapsule).start()

    #========================= SENDERS ====================#
    def TxGain(self):
        while(self.running):
            if(self.ping_state == "connected"):
                self.send('* GET 1 AUDIO_GAIN *')
                self.send('* GET 2 AUDIO_GAIN *')
            sleep(TRANSMITTER_TIME)
    
    def TxMute(self):
        while(self.running):
            if(self.ping_state == "connected"):
                self.send('* GET 1 MUTE *')
                self.send('* GET 2 MUTE *')
            sleep(TRANSMITTER_TIME)

    def TxGroup(self):
        while(self.running):
            if(self.ping_state == "connected"):
                self.send('* GET 1 GROUP_CHAN *')
                self.send('* GET 2 GROUP_CHAN *')
            sleep(TRANSMITTER_TIME)

    def TxBattery(self):
        while(self.running):
            if(self.ping_state == "connected"):
                self.send('* GET 1 TX_BAT *')
                self.send('* GET 2 TX_BAT *')
            sleep(TRANSMITTER_TIME)
    
    def TxCapsule(self):
        while(self.running):
            if(self.ping_state == "connected"):
                self.send('* GET 1 TX_TYPE *')
                self.send('* GET 2 TX_TYPE *')
            sleep(TRANSMITTER_TIME)

    def TxMetering(self):
        print("iniciando metering")
        self.send('* METER 2 ALL STOP *')
        self.send('* METER 2 ALL sss *')
        # while(self.running):
        #     #if(self.ping_state == "connected"):
        #     self.send('* METER 1 ALL sss *')
        #     #self.send('* METER 2 ALL sss *')
            

    #========================= RECEIVE ====================#
    @staticmethod
    def mute(data):
        if("OFF" in data): return False
        else: return True

    @staticmethod
    def isOnline(data):
        if("U" in data): return False
        else: return True

    def receiver(self):
        while(self.running):

            try: data, addr = self.read()
            except: data, addr = [0, 0]

            if((addr == self.answer_addr) and (data != 0)):
                data = data.split()

                #----------------------------- NAME ---------------------------#
                if("CHAN_NAME" in data[3]):
                    #......................... PING ...........................#
                    self.recv_ping = time()
                    self.checkDeltaState()
                    self.dev.ping = self.ping_state

                    if("1" in data[2]):
                        self.rx1.alias = str(data[4])

                    elif("2" in data[2]):
                        self.rx2.alias = str(data[4])

                #----------------------------- METERING -----------------------#
                elif("ALL" in data[3]):
                    # nn = diversity
                    # aaa = value of the RF level A
                    # bbb = value of the RF level B
                    # d = battery level
                    # eee = audio level (000-255)
                    print(
                    f"nn = {data[4]} | aaa = {data[5]} | bbb = {data[6]} | d = {data[7]} | eee = {data[8]}" 
                    )

                    # if("1" in data[2]):
                    #     self.rx1.gain = data[4]

                    # elif("2" in data[2]):
                    #     self.rx2.gain = data[4]

                #----------------------------- GAIN ---------------------------#
                elif("AUDIO_GAIN" in data[3]):
                    if("1" in data[2]):
                        self.rx1.gain = data[4]

                    elif("2" in data[2]):
                        self.rx2.gain = data[4]
                
                #----------------------------- MUTE ---------------------------#
                elif("MUTE" in data[3]):
                    if("1" in data[2]):
                        self.rx1.mute = self.mute(data[4])

                    elif("2" in data[2]):
                        self.rx2.mute = self.mute(data[4])
                
                #----------------------------- GROUP --------------------------#
                elif("GROUP_CHAN" in data[3]):
                    if("1" in data[2]):
                        self.rx1.group = (data[4], data["value2"])

                    elif("2" in data[2]):
                        self.rx2.group = (data[4], data["value2"])
                
                #----------------------------- FREQ ---------------------------#
                elif("FREQUENCY" in data[3]):
                    if("1" in data[2]):
                        self.rx1.carrier = data[4]

                    elif("2" in data[2]):
                        self.rx2.carrier = data[4]
                
                #----------------------------- BATTERY ------------------------#
                elif("TX_BAT" in data[3]):
                    if("1" in data[2]):
                        self.rx1.is_online = self.isOnline(data[4])
                        self.rx1.battery = data[4]

                    elif("2" in data[2]):
                        self.rx2.is_online = self.isOnline(data[4])
                        self.rx2.battery = data[4]
                
                #----------------------------- TYPE ---------------------------#
                elif("TX_TYPE" in data[3]):
                    if("1" in data[2]):
                        self.rx1.capsule = data[4]

                    elif("2" in data[2]):
                        self.rx2.capsule = data[4]