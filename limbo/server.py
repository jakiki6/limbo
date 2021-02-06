import socket, threading, json, base64, os
from . import packets

from .packets.handshake.serverbound import HandShakePacket
from .packets.status.serverbound import RequestPacket, PingPacket
from .packets.status.clientbound import ResponsePacket, PongPacket
from .packets.login.serverbound import LoginStartPacket
from .packets.login.clientbound import LoginDisconnectPacket

from .types import String

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "icon.png"), "rb") as file:
    icon = base64.b64encode(file.read()).decode()

class Client(threading.Thread):
    def __init__(self, sock, address, server):
        super().__init__()
        self.socket = sock
        self.address = address
        self.server = server
        self.state = 0
        self.start()
    def run(self):
        try:
            while True:
                buf = self.socket.recv(2097151)
                if len(buf) == 0:
                    break
                self.handle(buf)
        except OSError:
            pass
        finally:
#            print(f"Connection with {self.address} died")
            toremove = []
            for client in self.server.clients:
                if client.address == self.address:
                    toremove.append(client)
            for client in toremove:
                self.server.clients.remove(client)
#            print(f"{self.address} disconnected")
    def handle(self, buf):
        if buf[0] == 0xfe and self.state == 0:
#            print("Got legacy ping")
            self.socket.close()
            return
        packet = packets.unpack(buf, self.state)
        if packet == None:
            return
        print(packet)

        if type(packet) == HandShakePacket:
#            print(f"Updating to state {packet.next_state.val}")
            self.state = packet.next_state.val
        elif type(packet) == RequestPacket:
#            print("Got request packet")
            spacket = ResponsePacket()
            spacket.json_response = String(json.dumps({
                "version": {
                    "name": "Limbo@1.16.5",
                    "protocol": 754
                },
                "players": {
                    "max": self.server.maxclients,
                    "online": len(self.server.clients),
                    "sample": []
                },
                "description": {
                    "text": "Limbo driven server"
                },
                "favicon": "data:image/png;base64," + icon
            }), 32767)
            buf = packets.pack(spacket)
            self.socket.send(buf)
        elif type(packet) == PingPacket:
            spacket = PongPacket()
            spacket.payload = packet.payload
            buf = packets.pack(spacket)
            self.socket.send(buf)
            self.socket.close()
        elif type(packet) == LoginStartPacket:
            print(f"{packet.name.val} joined")
            spacket = LoginDisconnectPacket()
            spacket.reason = String(json.dumps({
                "text": f"Playing currently not supported {packet.name.val}"
            }), 32767)
            buf = packets.pack(spacket)
            self.socket.send(buf)
            self.socket.close()

class Server(threading.Thread):
    def __init__(self, host, port, maxclients):
        super().__init__()

        self.host = host
        self.port = port
        self.maxclients = maxclients

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.socket.listen(maxclients)

        self.clients = []
    def run(self):
        while True:
            client_socket, address = self.socket.accept()
#            print(f"{address} connected")
            self.clients.append(Client(client_socket, address, self))
