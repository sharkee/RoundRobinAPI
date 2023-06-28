import requests

from datetime import datetime
from router.constants import HEARTBEAT_MAX_LIFE

class Node:
    url = ""
    lastHeartbeat = None
    
    def __init__(self, url):
        self.url = url
        self.lastHeartbeat = datetime.now()

    def heartbeat(self):
        self.lastHeartbeat = datetime.now()
        return
        
    def isAlive(self):
        currTime = datetime.now()
        diff = (currTime - self.lastHeartbeat).total_seconds()
        return (diff < HEARTBEAT_MAX_LIFE)
        
    def post(self, jsonObj):
        return requests.post(self.url, json=jsonObj)