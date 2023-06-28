import requests
from router.constants import *

class RouterClient:
    url = ""
    routerUrl = ""
    
    def __init__(self, url, routerUrl):
        self.url = url
        self.routerUrl = routerUrl
        
    def connect(self):
        message = {
            "command" : "connect",
            "data" : {
                "url" : self.url
            }
        }
        return requests.post(self.routerUrl + CONNECT_NODE_API, json=message)

    def disconnect(self):
        message = {
            "command" : "disconnect",
            "data" : {
                "url" : self.url
            }
        }
        return requests.post(self.routerUrl + DISCONNECT_NODE_API, json=message)
        
    def sendHeartbeat(self):
        message = {
            "command" : "heartbeat",
            "data" : {
                "url" : self.url
            }
        }
        return requests.post(self.routerUrl + HEARTBEAT_NODE_API, json=message)