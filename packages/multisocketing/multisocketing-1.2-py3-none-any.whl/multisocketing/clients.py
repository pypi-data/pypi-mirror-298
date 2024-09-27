from . import packets as packetClasses
import socket
import json
from . import BYTES

class Client:
    def __init__(self, loop = None):
        self.connected = False
        self.connectedTo = None

        self.socket = None

        self.loopCB = loop

        self.packets = []

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Base class for clients
        # inherit from this if it does not meet your needs
    
    def registerPacket(self, packet):
        self.packets.append(packet)

    def disconnect(self):
        if not self.connected: # No need to disconnect if not connected
            return
        
        self.connected = False
        self.connectedTo = None
        
        self.socket.close() # Didn't know how to re-initialize the socket, So just replacing it with a new one
        del self.socket

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def log(self, msg):
        print(f"CLIENT | {msg}") # Logging

    def connect(self, host = "127.0.0.1", port = 5000):
        self.disconnect() # Disconnect if already connected

        self.socket.connect((host, port))

        self.connected = True
        self.connectedTo = (host, port)

        self.log(f"Connected to {host}:{port}")

        recvPackets = []

        while True:
            try:
                data = self.socket.recv(BYTES) # Recieving data
            except (ConnectionResetError, BrokenPipeError):
                # Server has probably crashed without warning
                self.disconnect()
                return

            if data: # Don't do anything if there is no data
                data = json.loads(data.decode())

                sentPackets = {}
                try:
                    sentPackets = data["packets"]
                except:
                    pass

                recvPackets = []
                for packet in sentPackets:
                    recvPackets.append(packetClasses.fromData(packet))
            
            if self.loopCB:
                result = self.loopCB(self, recvPackets)

                if result and isinstance(result, packetClasses.Packet):
                    result = [result]

                try:
                    self.packets.extend(result)
                except:
                    pass

            recvPackets = []

            data = {"packets": []}

            for packet in self.packets:
                data["packets"].append(packet.data())
            
            self.packets = []

            self.socket.send(json.dumps(data).encode()) # Send all packets to the server