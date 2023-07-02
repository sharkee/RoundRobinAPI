import json
import threading
from router.node import Node
from router.synchronized import synchronized_with_attr

class Router:
    nodeTable = []
    nodeTablelock = threading.RLock()
    
    @synchronized_with_attr("nodeTablelock")
    def getNumNodes(self):
        return len(self.nodeTable)
    
    @synchronized_with_attr("nodeTablelock")
    def getNode(self, url):
        for node in self.nodeTable:
            if node.url == url:
                return node
        return None
        
    @synchronized_with_attr("nodeTablelock")
    def getNodeByIdx(self, idx):
        return self.nodeTable[idx]
        
    @synchronized_with_attr("nodeTablelock")
    def addNode(self, url):
        self.nodeTable.append(Node(url))
        
    @synchronized_with_attr("nodeTablelock")
    def removeNode(self, url):
        for idx, node in enumerate(self.nodeTable):
            if url == node.url:
                del self.nodeTable[idx]
                return idx
        return -1
        
    @synchronized_with_attr("nodeTablelock")
    def removeDeadNodes(self):
        self.nodeTable[:] = [node for node in self.nodeTable if node.isAlive()]

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
        
    @synchronized_with_attr("nodeTablelock")
    def processInfo(self):
        # return total requests handled per node
        result = []
        for node in self.nodeTable:
            result.append({
                "url":node.url,
                "numPosts":node.numPosts,
                "minAverage":node.minAverage,
                "numPostsAtMin":node.numPostsAtMin,
                "maxAverage":node.maxAverage,
                "numPostsAtMax":node.numPostsAtMax,
                "custom":""
            })
        return result
        
    def rerouteMessage(self, jsonObj):
        node = self.getRerouteNode()
        if node != None:
            return node.post(jsonObj)
        return None
    
    # must be overridden by derived classes
    def getRerouteNode():
        return None