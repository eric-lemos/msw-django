from backend.views import views
from configs.settings import ENDPOINTS
from datetime import timedelta
from threading import Thread
from time import time, sleep
from json import loads
import requests

class Monitor:
    def __init__(self):
        self.url = "http://127.0.0.1:5000/"
        self.is_online = False
        self.save_back = False
        self.save_excp = True
        self.status_code = 0
        self.running = True
        self.message = ""
        self.seconds = 0
        self._uptime = 0
        self.start()

    @property
    def uptime(self):
        return self._uptime
    
    @uptime.setter
    def uptime(self, value):
        if(self.uptime != value):
            self._uptime = value

    def working(self):
        while(self.running):

            try:
                response = requests.get(self.url)
                data = loads(response.content)
                self.message = "It's all right!"
                self.seconds = data["uptime_secs"]
                self.uptime = str(timedelta(seconds=self.seconds))
                if(self.save_back): views.monitor.working.success(self.message)
                self.save_back = False
                self.save_excp = True
                self.is_online = True
                
            except requests.exceptions.Timeout:
                self.message = "The connection timed out. Trying to connect..."
                if(self.save_excp): views.monitor.working.exception(self.message)
                self.save_excp = False
                self.is_online = False
                self.save_back = True
                self.seconds = 0
                self.uptime = 0

            except requests.exceptions.TooManyRedirects:
                self.message = "A url you are trying to monitor is invalid."
                if(self.save_excp): views.monitor.working.exception(self.message)
                self.save_excp = False
                self.is_online = False
                self.save_back = True
                self.seconds = 0
                self.uptime = 0

            except requests.exceptions.RequestException as e:
                self.message = "The API is offline."
                if(self.save_excp): views.monitor.working.exception(self.message, e)
                self.save_excp = False
                self.is_online = False
                self.save_back = True
                self.seconds = 0
                self.uptime = 0

            sleep(1)
    
    def report(self):
        return {
            "system": "MSW-backend",
            "message": self.message,
            "uptime": self.uptime,
            "uptime_secs": self.seconds, 
            "is_online": int(self.is_online),
        }
    
    def start(self):
        Thread(target=self.working).start()

    def __del__(self):
        self.running = False

class Uptime:
    def __init__(self):
        self.started = time()
        self.running = True
        self.seconds = 0
        self.start()

    def working(self):
        while(self.running):
            self.seconds = int(time()-self.started)
            sleep(1)

    def report(self):
        return {
            "system": "MSW-backend",
            "uptime_secs": self.seconds,
        }

    def start(self):
        Thread(target=self.working).start()

    def __del__(self):
        self.running = False