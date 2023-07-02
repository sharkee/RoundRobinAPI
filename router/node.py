import requests

from datetime import datetime
from router.constants import HEARTBEAT_MAX_LIFE

class Node:
    url = ""
    lastHeartbeat = None
    
    # attributes to track performance
    numPosts = 0
    
    # track the performance of the node for the last 10 requests
    averagePostTime_last10 = 0
    totalPostTime_last10 = 0
    
    # track the minimum perf average
    minAverage = 100000
    numPostsAtMin = 0
    maxAverage = 0
    numPostsAtMax = 0
    
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
        self.totalPostTime_last10 += duration
        self.numPosts += 1
        
        if self.numPosts % 10 == 0:
            # perf metrics for last 10 requests
            self.averagePostTime_last10 = self.totalPostTime_last10 / 10
            if self.minAverage > self.averagePostTime_last10:
               self.minAverage = self.averagePostTime_last10
               self.numPostsAtMin = self.numPosts
            if self.maxAverage < self.averagePostTime_last10:
                self.maxAverage = self.averagePostTime_last10
                self.numPostsAtMax = self.numPosts
            self.totalPostTime_last10 = 0
        
        return response