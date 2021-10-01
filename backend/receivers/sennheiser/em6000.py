from configs.settings import TRANSMITTER_TIME, SUBSCRIBE_TIME
from backend.receivers.sennheiser._ping import Sennheiser
from backend.events import Device, Receive
from backend.models import Mics, Models
from backend.views import views
from threading import Thread
from time import time, sleep

class em6000(Sennheiser):
    def __init__(self, id, host, port, model, alias):
        super().__init__(host, port)
        self.init(id, model, alias)
        self.threads()

    #========================= STREAMING ==================#
    #------------------------- OVERVIEW -------------------#
    def getOverview(self):
        return {
            "device": self.dev.overview(),
            "receivers": {
                "rx1": self.rx1.overview(), 
                "rx2": self.rx2.overview()
            }
        }

    #------------------------- AUDIT ----------------------#
    #~~~~~~~~~~~~~~~~~~~~~~~~~ GET ~~~~~~~~~~~~~~~~~~~~~~~~#
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
        else: views.streaming.audit.get()

    #~~~~~~~~~~~~~~~~~~~~~~~~~ POST ~~~~~~~~~~~~~~~~~~~~~~~#
    def postAudit(self, mic, command, value):
        ###################### COMMANDS ####################
        if(command == "gain"):
            #................. GAIN .......................#
            if(mic == self.rx1.id): self.post({"audio":{"out1":{"level_db": int(value)}}})
            if(mic == self.rx2.id): self.post({"audio":{"out2":{"level_db": int(value)}}})

        return {"status": "success"}

    def getZabbix(self, device, mic):
        #--------------------- ZABBIX ---------------------#
        if((device == self.dev.id) and (mic == self.rx1.id)): return self.rx1.zabbix(self.dev.ping)
        elif((device == self.dev.id) and (mic == self.rx2.id)): return self.rx2.zabbix(self.dev.ping)
        else: views.streaming.zabbix.get()

    #========================= SENDERS ====================#
    def checkName(self):
        #--------------------- RX-NAME --------------------#
        while(self.running):
            if(self.ping_state == "connected"):
                self.send('{"rx1":{"skx":{"name":null}}}')
                self.send('{"rx2":{"skx":{"name":null}}}')
            sleep(TRANSMITTER_TIME)

    def checkMute(self):
        #--------------------- RX-MUTE --------------------#
        while(self.running):
            if(self.ping_state == "connected"):
                self.send('{"rx1":{"audio_mute":null}}')
                self.send('{"rx2":{"audio_mute":null}}')
            sleep(TRANSMITTER_TIME)

    def checkGain(self):
        #--------------------- RX-GAIN --------------------#
        while(self.running):
            if(self.ping_state == "connected"):
                self.send('{"rx1":{"skx":{"gain":null}}}')
                self.send('{"rx2":{"skx":{"gain":null}}}')
            sleep(TRANSMITTER_TIME)

    def checkLevel(self):
        #--------------------- RX-LEVEL -------------------#
        while(self.running):
            if(self.ping_state == "connected"):
                self.send('{"audio":{"out1":{"level_db":null}}}')
                self.send('{"audio":{"out2":{"level_db":null}}}')
            sleep(TRANSMITTER_TIME)

    def checkStatus(self):
        #--------------------- RX-STATUS ------------------#
        while(self.running):
            if(self.ping_state == "connected"):
                self.send('{"rx1":{"active_status":null}}')
                self.send('{"rx2":{"active_status":null}}')
            sleep(TRANSMITTER_TIME)

    def checkCarrier(self):
        #--------------------- RX-CARRIER -----------------#
        while(self.running):
            if(self.ping_state == "connected"):
                self.send('{"rx1":{"carrier":null}}')
                self.send('{"rx2":{"carrier":null}}')
            sleep(TRANSMITTER_TIME)
    
    def checkBattery(self):
        #--------------------- RX-BATTERY -----------------#
        while(self.running):
            if(self.ping_state == "connected"):
                self.send('{"rx1":{"skx":{"battery":null}}}')
                self.send('{"rx2":{"skx":{"battery":null}}}')
            sleep(TRANSMITTER_TIME)
    
    def checkCapsule(self):
        #--------------------- RX-CAPSULE -----------------#
        while(self.running):
            if(self.ping_state == "connected"):
                self.send('{"rx1":{"skx":{"capsule":null}}}')
                self.send('{"rx2":{"skx":{"capsule":null}}}')
            sleep(TRANSMITTER_TIME)
    
    def checkMetering(self):
        #--------------------- RX-METERING ----------------#
        while(self.running):
            if(self.ping_state == "connected"):
                self.send('{"osc":{"state":{"subscribe":[{"#":{"min":480,"max":480,"lifetime":15,"count":1000},"mm":null}]}}}')
            sleep(SUBSCRIBE_TIME)

    def checkWarnings(self):
        #--------------------- RX-WARNINGS ----------------#
        while(self.running):
            if(self.ping_state == "connected"):
                self.send('{"rx1":{"active_warnings":null}}')
                self.send('{"rx2":{"active_warnings":null}}')
            sleep(TRANSMITTER_TIME)
    
    def checkSysName(self):
        #--------------------- SYS-NAME -------------------#
        while(self.running):
            if(self.ping_state == "connected"):
                self.send('{"device":{"name":null}}')
            sleep(TRANSMITTER_TIME)

    def checkClockF(self):
        #--------------------- SYS-CLOCK-FREQ -------------#
        while(self.running):
            if(self.ping_state == "connected"):
                self.send('{"sys":{"clock_frequency_measured":null}}')
            sleep(TRANSMITTER_TIME)

    def checkClock(self):
        #--------------------- SYS-CLOCK ------------------#
        while(self.running):
            if(self.ping_state == "connected"):
                self.send('{"sys":{"clock":null}}')
            sleep(TRANSMITTER_TIME)

    #========================= RECEIVE ====================#
    def receiver(self):
        while(self.running):
            try: data, addr = self.read()
            except: data, addr = [0, 0]

            if((addr == self.address) and (data != 0)):
                #----------------------------- PING -----------------------#
                ping = self.mapping(data, args=["osc", "ping"])
                if((ping != None) and (ping == data["osc"]["ping"])):
                    self.recv_ping = time()
                    self.checkDeltaState()
                    self.dev.ping = self.ping_state

                else:
                    #------------------------- RX-METERING ----------------#
                    mm = self.mapping(data, args=["mm"])
                    if((mm != None) and (mm == data["mm"])):
                        self.rx1.audio = self.dBFS(mm[0][7])
                        self.rx1.rfa = self.dBm(mm[0][0])
                        self.rx1.rfb = self.dBm(mm[0][2])
                        self.rx1.lqi = self.lqi(mm[0][6])
                        self.rx1.dva = mm[0][4]
                        self.rx1.dvb = mm[0][5]
                        
                        self.rx2.audio = self.dBFS(mm[1][7])
                        self.rx2.rfa = self.dBm(mm[1][0])
                        self.rx2.rfb = self.dBm(mm[1][2])
                        self.rx2.lqi = self.lqi(mm[1][6])
                        self.rx2.dva = mm[1][4]
                        self.rx2.dvb = mm[1][5]
                    
                    #------------------------- RX-BATTERY -----------------#
                    rx1_battery = self.mapping(data, args=["rx1", "skx", "battery"])  
                    if((rx1_battery != None) and (rx1_battery == data["rx1"]["skx"]["battery"])):
                        self.rx1.battery = rx1_battery

                    rx2_battery = self.mapping(data, args=["rx2", "skx", "battery"]) 
                    if((rx2_battery != None) and (rx2_battery == data["rx2"]["skx"]["battery"])):
                        self.rx2.battery = rx2_battery

                    #------------------------- RX-WARNINGS ----------------#
                    rx1_warnings = self.mapping(data, args=["rx1", "active_warnings"])      
                    if((rx1_warnings != None) and (rx1_warnings == data["rx1"]["active_warnings"])):
                        self.rx1.is_online = self.CheckLink(rx1_warnings)
                        self.rx1.warnings = rx1_warnings

                    rx2_warnings = self.mapping(data, args=["rx2", "active_warnings"]) 
                    if((rx2_warnings != None) and (rx2_warnings == data["rx2"]["active_warnings"])):
                        self.rx2.is_online = self.CheckLink(rx2_warnings)
                        self.rx2.warnings = rx2_warnings

                    #------------------------- RX-ALIAS -------------------#
                    rx1_alias = self.mapping(data, args=["rx1", "skx", "name"])
                    if((rx1_alias != None) and (rx1_alias == data["rx1"]["skx"]["name"])):
                        self.rx1.alias = rx1_alias

                    rx2_alias = self.mapping(data, args=["rx2", "skx", "name"])
                    if((rx2_alias != None) and (rx2_alias == data["rx2"]["skx"]["name"])):
                        self.rx2.alias = rx2_alias

                    #------------------------- RX-GAIN --------------------#
                    rx1_gain = self.mapping(data, args=["rx1", "skx", "gain"])
                    if((rx1_gain != None) and (rx1_gain == data["rx1"]["skx"]["gain"])):
                        self.rx1.gain = rx1_gain

                    rx2_gain = self.mapping(data, args=["rx2", "skx", "gain"])
                    if((rx2_gain != None) and (rx2_gain == data["rx2"]["skx"]["gain"])):
                        self.rx2.gain = rx2_gain

                    #------------------------- RX-LEVEL -------------------#
                    rx1_level = self.mapping(data, args=["audio", "out1", "level_db"])
                    if((rx1_level != None) and (rx1_level == data["audio"]["out1"]["level_db"])):
                        self.rx1.level = rx1_level

                    rx2_level = self.mapping(data, args=["audio", "out2", "level_db"])
                    if((rx2_level != None) and (rx2_level == data["audio"]["out2"]["level_db"])):
                        self.rx2.level = rx2_level
                    
                    #------------------------- RX-STATUS ------------------#
                    rx1_status = self.mapping(data, args=["rx1", "active_status"])
                    if((rx1_status != None) and (rx1_status == data["rx1"]["active_status"])):
                        self.rx1.status = rx1_status

                    rx2_status = self.mapping(data, args=["rx2", "active_status"])
                    if((rx2_status != None) and (rx2_status == data["rx2"]["active_status"])):
                        self.rx2.status = rx2_status

                    #------------------------- RX-CARRIER -----------------#
                    rx1_carrier = self.mapping(data, args=["rx1", "carrier"])
                    if((rx1_carrier != None) and (rx1_carrier == data["rx1"]["carrier"])):
                        self.rx1.carrier = rx1_carrier

                    rx2_carrier = self.mapping(data, args=["rx2", "carrier"])
                    if((rx2_carrier != None) and (rx2_carrier == data["rx2"]["carrier"])):
                        self.rx2.carrier = rx2_carrier

                    #------------------------- RX-MUTE --------------------#
                    rx1_mute = self.mapping(data, args=["rx1", "audio_mute"])
                    if((rx1_mute != None) and (rx1_mute == data["rx1"]["audio_mute"])):
                        self.rx1.mute = rx1_mute

                    rx2_mute = self.mapping(data, args=["rx2", "audio_mute"])
                    if((rx2_mute != None) and (rx2_mute == data["rx2"]["audio_mute"])):
                        self.rx2.mute = rx2_mute

                    #------------------------- RX-CAPSULE -----------------#
                    rx1_capsule = self.mapping(data, args=["rx1", "skx", "capsule"])      
                    if((rx1_capsule != None) and (rx1_capsule == data["rx1"]["skx"]["capsule"])):
                        self.rx1.capsule  = rx1_capsule

                    rx2_capsule = self.mapping(data, args=["rx2", "skx", "capsule"]) 
                    if((rx2_capsule != None) and (rx2_capsule == data["rx2"]["skx"]["capsule"])):
                        self.rx2.capsule  = rx2_capsule

                    #------------------------- SYS-NAME -------------------#
                    dev_name = self.mapping(data, args=["device", "name"])
                    if((dev_name != None) and (dev_name == data["device"]["name"])):
                        self.dev.name = dev_name
                    
                    #------------------------- SYS-CLOCK-FREQ -------------#
                    dev_clock_freq = self.mapping(data, args=["sys", "clock_frequency_measured"])
                    if((dev_clock_freq != None) and (dev_clock_freq == data["sys"]["clock_frequency_measured"])):
                        self.dev.clock_freq = dev_clock_freq

                    #------------------------- SYS-CLOCK ------------------#
                    dev_clock = self.mapping(data, args=["sys", "clock"])
                    if((dev_clock != None) and (dev_clock == data["sys"]["clock"])):
                        self.dev.clock = dev_clock

    #========================= AUXILIARY ==================#
    @staticmethod
    def mapping(data, args=[]):
        #--------------------- MAPPING --------------------#
        index = 0
        items = len(args)
        if(args[index] not in data): pass
        else:
            while(items > index):
                for key in data.keys():
                    if(args[index] != key): index = items
                    else:
                        index += 1
                        data = data[key]
                        if(index >= items): 
                            return data
                 
    @staticmethod
    def CheckLink(warnings):
        #--------------------- CHECK-LINK -----------------#
        if("NoLink" in warnings): return False
        else: return True

    @staticmethod
    def lqi(value):
        #--------------------- LQI-CALC -------------------#
        return round((value/255)*100, 0)

    @staticmethod
    def dBFS(value): 
        #--------------------- DBFS-CALC ------------------#
        return (((value+1)/2)-128)

    @staticmethod
    def dBm(value):
        #--------------------- DBM-CALC -------------------#
        return ((value-255)/2)

    #========================= CONSTRUCTOR ================#
    def init(self, id, model, alias):
        #--------------------- INIT -----------------------#
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
        #--------------------- PARAMS ---------------------#
        params = Models.objects.order_by("id").filter(
            model=self.dev.model.upper())

        if(params):
            for param in params:
                self.dev.max_audio = param.max_aud
                self.dev.min_audio = param.min_aud
                self.dev.max_gain = param.max_gain
                self.dev.min_gain = param.min_gain
                self.dev.max_rf = param.max_rf
                self.dev.min_rf = param.min_rf

    def mics(self):
        #--------------------- MICS -----------------------#
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
        #--------------------- THREADS --------------------#
        Thread(target=self.ping).start()
        Thread(target=self.checkName).start()
        Thread(target=self.checkMute).start()
        Thread(target=self.checkGain).start()
        Thread(target=self.checkLevel).start()
        Thread(target=self.checkStatus).start()
        Thread(target=self.checkCarrier).start()
        Thread(target=self.checkBattery).start()
        Thread(target=self.checkCapsule).start()
        Thread(target=self.checkMetering).start()
        Thread(target=self.checkWarnings).start()
        Thread(target=self.checkSysName).start()
        Thread(target=self.checkClockF).start()
        Thread(target=self.checkClock).start()
        Thread(target=self.receiver).start()

#============================= END ========================#