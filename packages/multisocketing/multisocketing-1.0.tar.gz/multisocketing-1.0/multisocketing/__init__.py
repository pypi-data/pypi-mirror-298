#__init__.py
"""
A simple library that lets you make socket servers and clients.
Handles all of the backend stuff so you can focus on your application.

To get started, You can make a server with a host and port, Then start it.
After that, Make a client and connect to that server.

If you want to send data, Make a class inheriting off of the Packet class.

If the Server and Client classes don't meet your needs, You can make classes
that inherit from those.
"""

BYTES = 1024

from . import *