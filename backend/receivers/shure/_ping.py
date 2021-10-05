from backend.protocols import Udp
from backend.views import views
from time import time, sleep

class Shure(Udp):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.ping_state = "not-configured"
        self.num_ping_received = 0
        self.max_ping_received = 2
        self.num_ping_lost = int(0)
        self.max_ping_lost = int(5)
        self.last_ping = 0
        self.recv_ping = 0

    @property
    def delta(self):
        if((self.recv_ping - self.last_ping) < 0): return -1
        return (self.recv_ping - self.last_ping)

    def checkDeltaState(self):
        if(self.delta < 0):
            if(self.num_ping_lost == self.max_ping_lost):
                self.num_ping_lost = self.max_ping_lost
                self.ping_state = "configured"
                self.num_ping_received = 0
            else:
                self.num_ping_lost += 1
                if(self.num_ping_lost == self.max_ping_lost):
                    views.ping.not_connected("Shure", self.address)
                    
        else:
            if(self.num_ping_received == self.max_ping_received):
                self.num_ping_received = self.max_ping_received
                self.ping_state = "connected"
                self.num_ping_lost = 0
            else:
                self.num_ping_received += 1
                if(self.num_ping_received == self.max_ping_received):
                    views.ping.connected("Shure", self.address)

    def ping(self):
        while(self.running):
            self.send('* GET 1 CHAN_NAME *')
            self.send('* GET 2 CHAN_NAME *')
            self.last_ping = time()
            self.checkDeltaState()
            sleep(1)