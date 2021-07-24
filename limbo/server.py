import socket, threading, json, base64, os, uuid, time
from . import packets, constants

from .packets.handshake.serverbound import HandShakePacket
from .packets.status.serverbound import RequestPacket, PingPacket
from .packets.status.clientbound import ResponsePacket, PongPacket
from .packets.login.serverbound import LoginStartPacket
from .packets.login.clientbound import LoginDisconnectPacket, LoginSuccessPacket
#from .packets.play.serverbound import 
from .packets.play.clientbound import JoinGamePacket

from .types import *

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
        print(f"<- {packet} ({len(buf)})")

        if type(packet) == HandShakePacket:
            print(f"Connection with client version {packet.protocol_version.val}")
#            print(f"Updating to state {packet.next_state.val}")
            self.state = packet.next_state.val
        elif type(packet) == RequestPacket:
#            print("Got request packet")
            spacket = ResponsePacket()
            spacket.json_response = String(json.dumps({
                "version": {
                    "name": "Limbo@1.17.1",
                    "protocol": 756
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
            packets.send(spacket, self.socket)
        elif type(packet) == PingPacket:
            spacket = PongPacket()
            spacket.payload = packet.payload
            packets.send(spacket, self.socket)
            self.socket.close()
        elif type(packet) == LoginStartPacket:
            print(f"{packet.name.val} joined")
#            spacket = LoginDisconnectPacket()
#            spacket.reason = String(json.dumps({
#                "text": f"Playing currently not supported {packet.name.val}"
#            }), 32767)
            spacket = LoginSuccessPacket()
            spacket.uuid = UUID()
            spacket.username = String(packet.name.val, 16)
            packets.send(spacket, self.socket)
            self.state = 3

            spacket = JoinGamePacket()
            spacket.entity_id = Int(0)
            spacket.is_hardcore = Boolean(True)
            spacket.gamemode = UnsignedByte(3)
            spacket.previous_gamemode = Byte(-1)
            spacket.world_count = VarInt(1)
            spacket.world_names = Array([
                Identifier("limbo:the")
            ])
            spacket.dimension_codec = NbtTagCompound(constants.dimension_codec)
            spacket.dimension = NbtTagCompound(constants.dimension)
            spacket.world_name = Identifier("limbo:the")
            spacket.hashed_seed = Long(0)
            spacket.max_players = VarInt(0)
            spacket.view_distance = VarInt(32)
            spacket.reduced_debug_info = Boolean(False)
            spacket.enable_respawn_screen = Boolean(True)
            spacket.is_debug = Boolean(False)
            spacket.is_flat = Boolean(False)
            packets.send(spacket, self.socket)

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
