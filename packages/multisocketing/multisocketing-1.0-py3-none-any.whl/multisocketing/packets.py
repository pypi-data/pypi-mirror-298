# packet.py
import json

def fromData(data):
    packet = eval(f"{data["type"]}()")
    for key in data:
        if key != "type":
            setattr(packet, key, data[key])
    
    return packet

class Packet:
    def __init__(self):
        pass

        # Base class for packets
        # inherit from this if you want to send data
        # between the client and server
    
    def data(self):
        data = {}

        data["type"] = type(self).__name__ # Set "type" to class name

        for attr in dir(self):
            if attr in ("__dict__", "__module__"): # These attributes are useless, So we save on precious bytes
                continue

            value = getattr(self, attr)

            if not type(value).__name__ in ("int", "float", "str", "bool", "dict", "list", "tuple"): # Only these types are supported
                continue

            data[attr] = value # For each attribute, Add it to the data
        
        return data

    def __bytes__(self):
        data = self.data()

        return json.dumps(data).encode()