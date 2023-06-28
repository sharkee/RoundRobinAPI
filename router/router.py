import json
from router.node import Node

class Router:
    nodeTable = []
    
    def getNode(self, url):
        for node in self.nodeTable:
            if node.url == url:
                return node
        return None
        
    def addNode(self, url):
        self.nodeTable.append(Node(url))
        
    def removeNode(self, url):
        for idx, node in enumerate(self.nodeTable):
            if url == node.url:
                del self.nodeTable[idx]
                break
        return

    def processNodeConnect(self, jsonObj):
        url = jsonObj["data"]["url"]
        # check if node is already in table
        node = self.getNode(url)
        if node != None:
            node.heartbeat() # keep alive
            return jsonObj
        self.addNode(url)
        return jsonObj, 201

    def processNodeDisconnect(self, jsonObj):
        url = jsonObj["data"]["url"]
        self.removeNode(url)
        return jsonObj

    def processNodeHeartbeat(self, jsonObj):
        url = jsonObj["data"]["url"]
        node = self.getNode(url)
        if node != None:
            node.heartbeat() # keep alive
        else:
            self.addNode(url)
        return jsonObj
        
    def rerouteMessage(self, jsonObj):
        node = self.getRerouteNode()
        if node != None:
            return node.post(jsonObj)
        return None
    
    # must be overridden by derived classes
    def getRerouteNode():
        return None