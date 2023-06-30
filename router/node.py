import requests

from datetime import datetime
from router.constants import HEARTBEAT_MAX_LIFE

class Node:
    url = ""
    lastHeartbeat = None
    averagePostTime = 0
    totalPostTime = 0
    numPosts = 0
    
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
        start = datetime.now()
        response = requests.post(self.url, json=jsonObj)
        end = datetime.now()
        
        # compute duration in ms
        duration = (end - start).total_seconds() * 1000
        
        # update node values
        self.totalPostTime += duration
        self.numPosts += 1
        self.averagePostTime = self.totalPostTime / self.numPosts
        
        return response