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