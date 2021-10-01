from backend.views import views
from json import loads
import socket as sock

class Protocol:
    def __init__(self, host, port):
        self.running = True
        self._host = host
        self._port = port
    
    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @host.setter
    def host(self, value):
        self._host = value

    @port.setter
    def port(self, value):
        self._port = value

    def post(self):
        views.protocol.post()

    def send(self):
        views.protocol.send()

    def read(self):
        views.protocol.read()

class Udp(Protocol):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.socket = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
        self.address = (self.host, self.port)
        self.socket.settimeout(2)

    def post(self, data):
        message = str(data).replace("'","\"").encode("utf-8")
        self.socket.sendto(message, self.address)

    def send(self, data):
        message = str(data).encode("utf-8")
        self.socket.sendto(message, self.address)

    def read(self):
        data, addr = self.socket.recvfrom(1024)
        data = loads(data.decode("utf-8"))
        return [data, addr]
    
    def __del__(self):
        self.socket.close()