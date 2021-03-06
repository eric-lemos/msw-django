from backend.logging import Logging
log = Logging("MSW-Backend")

class views:
    
    class protocol:
    #========================= PROTOCOL ===================#
        @staticmethod
        def post():
            value = "Method 'post' not defined."
            log.info(subsys="Protocol.post", desc=value)
        
        @staticmethod
        def send():
            value = "Method 'send' not defined."
            log.info(subsys="Protocol.send", desc=value)
        
        @staticmethod
        def read():
            value = "Method 'read' not defined."
            log.info(subsys="Protocol.read", desc=value)
    
    class ping:
    #========================= PING =======================#
        @staticmethod
        def connected(model, addr):
            value = f"Connection established {addr}"
            log.info(subsys=f"{model}.checkDeltaState", desc=value, save=True)

        @staticmethod
        def not_connected(model, addr):
            value = f"Lost connection {addr}"
            log.info(subsys=f"{model}.checkDeltaState", desc=value, save=True)

    class event:
    #========================= EVENTS =====================#   
        #--------------------- DEVICE ---------------------#
        class device:
            @staticmethod
            def ping(value):
                log.debug(subsys="Device.ping", desc=value)

            @staticmethod
            def name(value):
                log.debug(subsys="Device.name", desc=value)

            @staticmethod
            def alias(value):
                log.debug(subsys="Device.alias", desc=value)

            @staticmethod
            def clock(value):
                log.debug(subsys="Device.clock", desc=value)

            @staticmethod
            def clock_freq(value):
                log.debug(subsys="Device.clock_freq", desc=value)

        #--------------------- RECEIVE --------------------#
        class receive:
            @staticmethod
            def id(value):
                log.debug(subsys="Receiver.id", desc=value)
            
            @staticmethod
            def rfa(value):
                log.debug(subsys="Receiver.rfa", desc=value)
            
            @staticmethod
            def rfb(value):
                log.debug(subsys="Receiver.rfb", desc=value)
            
            @staticmethod
            def dva(value):
                log.debug(subsys="Receiver.dva", desc=value)
            
            @staticmethod
            def dvb(value):
                log.debug(subsys="Receiver.dvb", desc=value)
            
            @staticmethod
            def lqi(value):
                log.debug(subsys="Receiver.lqi", desc=value)
            
            @staticmethod
            def name(value):
                log.debug(subsys="Receiver.name", desc=value)

            @staticmethod
            def gain(value):
                log.debug(subsys="Receiver.gain", desc=value)
            
            @staticmethod
            def mute(value):
                log.debug(subsys="Receiver.mute", desc=value)

            @staticmethod
            def group(value):
                log.debug(subsys="Receiver.group", desc=value)

            @staticmethod
            def audio(value):
                log.debug(subsys="Receiver.audio", desc=value)
            
            @staticmethod
            def level(value):
                log.debug(subsys="Receiver.level", desc=value)
            
            @staticmethod
            def alias(value):
                log.debug(subsys="Receiver.alias", desc=value)
            
            @staticmethod
            def detail(value):
                log.debug(subsys="Receiver.detail", desc=value)
            
            @staticmethod
            def status(value):
                log.debug(subsys="Receiver.status", desc=value)
            
            @staticmethod
            def carrier(value):
                log.debug(subsys="Receiver.carrier", desc=value)
            
            @staticmethod
            def battery(value):
                log.debug(subsys="Receiver.battery", desc=value)
            
            @staticmethod
            def capsule(value):
                log.debug(subsys="Receiver.capsule", desc=value)
            
            @staticmethod
            def warnings(value):
                log.debug(subsys="Receiver.warnings", desc=value)
            
            @staticmethod
            def is_online(status, detail, name, alias):
                if(status == True): value = f"[{detail.upper()}] Microphone {name} '{alias}' has been turned on"
                else: value = f"[{detail.upper()}] Microphone {name} '{alias}' has been turned off"
                log.info(subsys="Receiver.is_online", desc=value, save=True)
    
    class audit:
    #========================= AUDIT ======================#
        @staticmethod
        def not_exist():
            value = "Requested microphone does not exist."
            log.error(subsys="Gateway.postAudit", desc=value)
            return value
        
        @staticmethod
        def null_object():
            value = "Error trying to change null object."
            log.error(subsys="Gateway.postAudit", desc=value)
            return value
        
        @staticmethod
        def out_range(model):
            value = "Value set out of range allowed by the device."
            log.warning(subsys=f"{model}.postAudit", desc=value)
            return value
    
    class gateway:
        @staticmethod
        def load(objects):
            value = f"Created objects: \n {objects} \n"
            log.info(subsys="Gateway.load", desc=value)

    class server:
    #========================= SERVER =====================#
        @staticmethod
        def started(server, port):
            value = f"WSGI serving on http://[::]:{port}"
            log.info(subsys=f"stream.{server}", desc=value, save=True)
            
        @staticmethod
        def keyInterrupt(server):
            value = "WSGI server was terminated from keyboard."
            log.warning(subsys=f"stream.{server}", desc=value, save=True)
        
        @staticmethod
        def exceptions(server, e):
            value = f"Error trying to start WSGI server. Exceptions: \n {e} \n\n"
            log.error(subsys=f"stream.{server}", desc=value, save=True)
    
    class monitor:
    #========================= MONITOR ====================#
        class working:
            def success(message):
                value = f"{message}"
                log.info(subsys=f"Monitor.working", desc=value, save=True)

            def exception(message, e=None):
                value = f"{message}"
                if(e != None): value += f" Exceptions: \n {e} \n"
                log.error(subsys=f"Monitor.working", desc=value, save=True)