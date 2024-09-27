# server.py
import packet as packetClasses
import json
import socket
import threading
from . import BYTES

class Server:
    def __init__(self, clientLoop = None, maxClients = 10, host = "127.0.0.1", port = 5000):
        # Base server class

        self.host = host
        self.port = port
        
        self.maxClients = maxClients
        self.connectedClients = 0

        self.clientLoopCB = clientLoop

        self.started = False

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.bind((self.host, self.port))

    def clientLoop(self, client, addr):
        packets = []
        recvPackets = []

        client.send(json.dumps({"packets": []}).encode())

        while True:
            try:
                data = client.recv(BYTES) # Recieving data
            except (ConnectionResetError, BrokenPipeError):
                # Client has probably crashed without warning
                self.log(f"Client from {addr[0]}:{addr[1]} disconnected")
                self.connectedClients -= 1
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
            
            if self.clientLoopCB:
                result = self.clientLoopCB(self, client, recvPackets)

                if result and isinstance(result, packetClasses.Packet):
                    result = [result]

                try:
                    packets.extend(result)
                except:
                    pass
            
            recvPackets = []

            data = {"packets": []}
            
            for packet in packets:
                data["packets"].append(packet.data())
            
            packets = []

            client.send(json.dumps(data).encode()) # Send all packets to the client

    def log(self, msg):
        print(f"SERVER | {msg}") # Logging

    def start(self):
        self.stop() # Stop if started already

        self.started = True

        self.socket.listen(self.maxClients)

        self.log(f"Listening at {self.host}:{self.port}")

        while True:
            conn, addr = self.socket.accept()

            self.log(f"Client connected from {addr[0]}:{addr[1]}")

            self.connectedClients += 1

            thread = threading.Thread(target=self.clientLoop, args=[conn, addr]) # Doing the traditional way of multiple clients
            thread.start()
    
    def stop(self):
        if not self.started: # No need to stop if not started
            return
        
        self.started = False

        self.socket.close() # Didn't know how to re-initialize the socket, So just replacing it with a new one
        del self.socket

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)