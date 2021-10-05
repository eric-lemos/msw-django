from backend.models import Mics
from backend.views import views

class Device:
    #========================= DEVICE =====================#
    def __init__(self):
        self._id = 0
        self._host = ""
        self._port = 0
        self._ping = "not-configured"
        self._name = ""
        self._alias = ""
        self._model = ""
        self._clock = 0
        self._clock_freq = 0
        self._max_audio = 0
        self._min_audio = 0
        self._max_gain = 0
        self._min_gain = 0
        self._max_rf = 0
        self._min_rf = 0

    def __str__(self):
        return self.alias

    #========================= STREAMING ==================#
    #------------------------- OVERVIEW -------------------#
    def overview(self):
        return {
            "id": self.id,
            "model": self.model,
            "alias": self.alias,
            "ping": self.ping,
        }

    #------------------------- AUDIT ----------------------#
    def audit(self):
        return {
            "id": self.id,
            "model": self.model,
            "alias": self.alias,
            "host": self.host,
            "port": self.port,
            "ping": self.ping,

            "feature": {
                "min_gain": self.min_gain,
                "max_gain": self.max_gain,
            },

            "system": {
                "name": self.name,
                "clock": self.clock,
                "clock_freq": self.clock_freq
            }
        }

    #========================= GETTERS ====================#
    @property
    def id(self):
        return self._id
    
    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port
    
    @property
    def ping(self):
        return self._ping

    @property
    def name(self):
        return self._name

    @property
    def alias(self):
        return self._alias
    
    @property
    def model(self):
        return self._model

    @property
    def clock(self):
        return self._clock

    @property
    def clock_freq(self):
        return self._clock_freq
    
    @property
    def max_audio(self):
        return self._max_audio

    @property
    def min_audio(self):
        return self._min_audio
    
    @property
    def max_gain(self):
        return self._max_gain
    
    @property
    def min_gain(self):
        return self._min_gain

    @property
    def max_rf(self):
        return self._max_rf

    @property
    def min_rf(self):
        return self._min_rf

    #========================= SETTERS ====================#
    @id.setter
    def id(self, value):
        if(self.id != value):
            self._id = value
    
    @host.setter
    def host(self, value):
        if(self.host != value):
            self._host = value

    @port.setter
    def port(self, value):
        if(self.port != value):
            self._port = value

    @model.setter
    def model(self, value):
        if(self.model != value):
            self._model = value

    @ping.setter
    def ping(self, value):
        if(self.ping != value):
            self._ping = value
            views.event.device.ping(self.ping)

    @name.setter
    def name(self, value):
        if(self.name != value):
            self._name = value
            views.event.device.name(self.name)
    
    @alias.setter
    def alias(self, value):
        if(self.alias != value): 
            self._alias = value
            views.event.device.alias(self.alias)

    @clock.setter
    def clock(self, value):
        if(self.clock != value):
            if(not value): self._clock = 0
            else: 
                self._clock = value
                views.event.device.clock(self.clock)

    @clock_freq.setter
    def clock_freq(self, value):
        if(self.clock_freq != value):
            if(not value): self._clock_freq = 0
            else:
                self._clock_freq = value
                views.event.device.clock_freq(self.clock_freq)
    
    @max_audio.setter
    def max_audio(self, value):
        if(self.max_audio != value):
            if(not value): self._max_audio = 0
            else: self._max_audio = value
    
    @min_audio.setter
    def min_audio(self, value):
        if(self.min_audio != value):
            if(not value): self._min_audio = 0
            else: self._min_audio = value

    @max_gain.setter
    def max_gain(self, value):
        if(self.max_gain != value):
            if(not value): self._max_gain = 0
            else: self._max_gain = value

    @min_gain.setter
    def min_gain(self, value):
        if(self.min_gain != value):
            if(not value): self._min_gain = 0
            else: self._min_gain = value
    
    @max_rf.setter
    def max_rf(self, value):
        if(self.max_rf != value):
            if(not value): self._max_rf = 0
            else: self._max_rf = value

    @min_rf.setter
    def min_rf(self, value):
        if(self.min_rf != value):
            if(not value): self._min_rf = 0
            else: self._min_rf = value

class Receive:
    #========================= RECEIVE ====================#
    def __init__(self, device):
        self._id = 0
        self._rfa = 0
        self._rfb = 0
        self._dva = 0
        self._dvb = 0
        self._lqi = 0
        self._name = ""
        self._gain = 0
        self._dev = device
        self._group = "unknown"
        self._mute = False
        self._audio = 0
        self._level = 0
        self._alias = ""
        self._detail = ""
        self._status = []
        self._carrier = 0
        self._battery = [0,0]
        self._capsule = ""
        self._warnings = []
        self._is_online = False
        self._audio_p = 0
        self._rfa_p = 0
        self._rfb_p = 0

    def __str__(self):
        return self.alias

    #========================= GETTERS ====================#
    @property
    def id(self): 
        return self._id

    @property
    def rfa(self): 
        return self._rfa
    
    @property
    def rfb(self): 
        return self._rfb

    @property
    def rfa_p(self): 
        return self._rfa_p

    @property
    def rfb_p(self): 
        return self._rfb_p

    @property
    def dva(self): 
        return self._dva

    @property
    def dvb(self): 
        return self._dvb

    @property
    def lqi(self): 
        return self._lqi

    @property
    def name(self): 
        return self._name
    
    @property
    def gain(self): 
        return self._gain

    @property
    def mute(self): 
        return self._mute

    @property
    def group(self): 
        return self._group

    @property
    def audio(self): 
        return self._audio
    
    @property
    def audio_p(self): 
        return self._audio_p

    @property
    def level(self): 
        return self._level

    @property
    def alias(self): 
        return self._alias
    
    @property
    def detail(self): 
        return self._detail

    @property
    def status(self): 
        return self._status

    @property
    def carrier(self): 
        return self._carrier

    @property
    def battery(self): 
        return self._battery

    @property
    def capsule(self): 
        return self._capsule

    @property
    def warnings(self): 
        return self._warnings

    @property
    def is_online(self): 
        return self._is_online

    #========================= SETTERS ====================#
    @id.setter
    def id(self, value):
        if(self.id != value): 
            self._id = value
    
    @rfa.setter
    def rfa(self, value):
        if(self.rfa != value): 
            if(not value): self._rfa = 0
            else:
                self._rfa = value
                self.rfa_p = value
            views.event.receive.rfa(self.rfa)

    @rfb.setter
    def rfb(self, value):
        if(self.rfb != value): 
            if(not value): self._rfb = 0
            else:
                self._rfb = value
                self.rfb_p = value
                views.event.receive.rfb(self.rfb)

    @rfa_p.setter
    def rfa_p(self, value):
        if(self.rfa_p != value):
            self._rfa_p = self.percent(value, self._dev.min_rf, self._dev.max_rf)
            #print(self.rfa_p)
    
    @rfb_p.setter
    def rfb_p(self, value):
        if(self.rfb_p != value):
            self._rfb_p = self.percent(value, self._dev.min_rf, self._dev.max_rf)

    @dva.setter
    def dva(self, value):
        if(self.dva != value):
            if(not value): self._dva = 0
            else: 
                self._dva = value
                views.event.receive.dva(self.dva)
    
    @dvb.setter
    def dvb(self, value):
        if(self.dvb != value): 
            if(not value): self._dvb = 0
            else: 
                self._dvb = value
                views.event.receive.dvb(self.dva)

    @lqi.setter
    def lqi(self, value):
        if(self.lqi != value):
            self._lqi = value
            views.event.receive.lqi(self.lqi)

    @name.setter
    def name(self, value):
        if(self.name != value):
            if(not value): self._name = ""
            else:
                self._name = value
                views.event.receive.name(self.name)

    @gain.setter
    def gain(self, value):
        if(self.gain != value): 
            if(not value): self._gain = 0
            else:
                self._gain = value
                views.event.receive.gain(self.gain)

    @mute.setter
    def mute(self, value):
        if(self.mute != value): 
            if(not value): self._mute = False
            else: 
                self._mute = value
                views.event.receive.mute(self.mute)

    @group.setter
    def group(self, value):
        if(self.group != value): 
            if(not value): self._group = "unknown"
            else:
                self._group = value
                views.event.receive.group(self.group)

    @audio.setter
    def audio(self, value):
        if(self.audio != value): 
            if(not value):
                self._audio = 0
            else: 
                self._audio = value
                self.audio_p = self.audio
                views.event.receive.audio(self.audio)

    @audio_p.setter
    def audio_p(self, value):
        if(self.audio_p != value): 
            if(not value): self._audio_p = 0
            else: self._audio_p = self.percent(value, self._dev.min_audio, self._dev.max_audio)

    @level.setter
    def level(self, value):
        if(self.level != value): 
            if(not value): self._level = 0
            else:
                self._level = value
                views.event.receive.level(self.level)

    @alias.setter
    def alias(self, value):
        if(self.id != 0):
            alias_query = Mics.objects.get(id=self.id)
            if(not value): self._alias = alias_query.alias
            else:
                value = value.rstrip()
                if(self.alias != value):
                    self._alias = value
                    alias_query.alias = value
                    views.event.receive.alias(value)
                    alias_query.save()

    @detail.setter
    def detail(self, value):
        if(self.detail != value): 
            if(not value): self._detail = ""
            else:
                self._detail = value
                views.event.receive.detail(self.detail)

    @status.setter
    def status(self, value):
        if(self.status != value): 
            self._status = value
            views.event.receive.status(self.status)

    @carrier.setter
    def carrier(self, value):
        if(self.carrier != value):
            if(not value): self._carrier = 0
            else: 
                self._carrier = value
                views.event.receive.carrier(self.carrier)
        
    @battery.setter
    def battery(self, value):
        if(self.battery != value):
            if(not value): self._battery = [0, 0]
            else:
                self._battery = value
                views.event.receive.battery(self.battery)

    @capsule.setter
    def capsule(self, value):
        if(self.capsule != value):
            if(not value): self._capsule = ""
            else:
                self._capsule = value
                views.event.receive.capsule(self.capsule)
    
    @warnings.setter
    def warnings(self, value):
        if(self.warnings != value):
            self._warnings = value
            views.event.receive.warnings(self.warnings)

    @is_online.setter
    def is_online(self, value):
        if((self.id !=0) and (self.alias != "")):
            if(self.is_online != value):
                self._is_online = value
                if(self.is_online): views.event.receive.is_online(True, self.detail, self.name, self.alias)
                else: views.event.receive.is_online(False, self.detail, self.name, self.alias)

    #========================= AUXILIAR ===================#
    #------------------------- PERCENT --------------------#
    @staticmethod
    def percent(value, min, max):
        return round( ((value - min)/(max - min))*100, 2)

    #------------------------- BATTERY-TIME ---------------#
    @property
    def battery_time(self):
        batteryTime = self.battery[1]
        if(batteryTime == "-:--" or not batteryTime): return 0
        else: return sum(x * int(t) for x, t in zip([3600, 60], batteryTime.split(":")))

    #------------------------- BATTERY-CHARGE -------------#
    @property
    def battery_charge(self):
        charge = self.battery[0] 
        if(charge == "100%"): return 100
        elif(charge == "70%"): return 70
        elif(charge == "30%"): return 30
        elif(charge == "low"): return 10
        else: return 0

    #------------------------- WARNINGS -------------------#
    def checkWarning(self, warning):
        if(warning in self.warnings): return 1
        else: return 0

    #------------------------- PING -----------------------#
    def checkPing(self, value):
        if(value == "connected"): return 1
        else: return 0


    #========================= STREAMING ==================#
    #------------------------- OVERVIEW -------------------#
    def overview(self):
        return {
            "id": self.id,
            "dva": self.dva,
            "dvb": self.dvb,
            "name": self.name,
            "alias": self.alias,
            "status": self.status,
            "battery": self.battery,
            "group": self.group,
            "carrier": self.carrier,
            "warnings": self.warnings,
            "is_online": self.is_online,
        }


    #------------------------- AUDIT ----------------------#
    def audit(self):
        return {
            "id": self.id,
            "rfa": self.rfa,
            "rfb": self.rfb,
            "dva": self.dva,
            "dvb": self.dvb,
            "lqi": self.lqi,
            "name": self.name,
            "mute": self.mute,
            "audio": self.audio,
            "level": self.level,
            "alias": self.alias,
            "detail": self.detail,
            "status": self.status,
            "group": self.group,
            "carrier": self.carrier,
            "battery": self.battery,
            "capsule": self.capsule,
            "warnings": self.warnings,
            "is_online": self.is_online,
            "audio_p": self.audio_p,
            "rfa_p": self.rfa_p,
            "rfb_p": self.rfb_p,
        }


    #========================= ZABBIX =====================#
    def zabbix(self, ping):
        return {
            "id": self.id,
            "name": self.name,
            "alias": self.alias,
            "detail": self.detail,
            "ping": self.checkPing(ping),
            "group": self.group,
            "carrier": self.carrier,
            "level_db": self.level,
            "audio": self.audio,
            "rf_a": self.rfa,
            "rf_b": self.rfb,
            "lqi": self.lqi,
            "capsule": self.capsule,
            "battery_time": self.battery_time,
            "battery_charge": self.battery_charge,
            "RFPeak": self.checkWarning("RFPeak"),
            "AFPeak": self.checkWarning("AFPeak"),
            "NoLink": self.checkWarning("NoLink"),
            "NoClock": self.checkWarning("NoClock"),
            "BadClock": self.checkWarning("BadClock"),
            "LowSignal": self.checkWarning("LowSignal"),
            "LowBattery": self.checkWarning("LowBattery"),
            "Aes256Error": self.checkWarning("Aes256Error"),
            "AnTxYBNCShorted": self.checkWarning("AnTxYBNCShorted"),
        }