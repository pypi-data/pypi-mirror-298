# Multisocket
A library that handles all of the socket backend, While you can focus on making your application.

It's easy to set it up, Just make a Server (multisocket.server.Server) and some Clients (multisocket.client.Client),
Start the server, And connect the clients to the server.

You can give the client or the server a callback function, So that you can change their behaviour!

If you give the client a callback function, It will be called every frame and be given these arguments.

client - The client that called this function.
packets - All of the packets that the client recieved from the server, In a list.

This callback function can return a single packet, Or a list of them, And the client will send them to the server.


Similarly, If you give the server a callback function, It will also be called every frame, And get these arguments.

server - The server that called this function.
client - The client that the packets will be sent to.
packets - All of the packets that the server recieved from the client, In a list.

This callback function can also return packets to send to the client.


This is a simple script that uses multisocket to communicate between servers and clients:
```python
from multisocketing import clients, servers
from multisocketing import packets as packetClasses
import threading

def clientLoop(client, packets):
    print("packets from server:")
    print(packets)
    return packetClasses.Packet()

def serverLoop(server, client, packets):
    print("packets from client:")
    print(packets)

def setupServer():
    s = servers.Server(Sloop)
    s.start()

def makeClient():
    c = clients.Client(Cloop)
    c.connect()

thread = threading.Thread(target=setupServer)
thread.start()

thread = threading.Thread(target=makeClient)
thread.start()

makeClient()
```

Hope this library makes it easier for you to make socket-related applications!