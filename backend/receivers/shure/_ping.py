from backend.protocols import Udp
from backend.views import views
from time import time, sleep

class Shure(Udp):
    def __init__(self, host, port):
        super().__init__(host, port)