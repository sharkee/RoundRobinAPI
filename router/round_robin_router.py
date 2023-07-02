import threading
from router.router import Router
from router.synchronized import synchronized_with_attr

class RoundRobinRouter(Router):
    currNodeIdx = -1
    currNodeIdxLock = threading.RLock()
    
    @synchronized_with_attr("currNodeIdxLock")
    def getCurrNodeIdx(self):
        return self.currNodeIdx
    
    @synchronized_with_attr("currNodeIdxLock")
    def setCurrNodeIdx(self, value):
        self.currNodeIdx = value
    
    @synchronized_with_attr("currNodeIdxLock")
    def removeNode(self, url):
        idx = super().removeNode(url)
        if idx >= 0:
            # update index tracker when necessary
            if self.currNodeIdx >= idx:
                self.currNodeIdx -= 1
        return idx

    @synchronized_with_attr("nodeTablelock")
    def getNextNode(self):
        numNodes = self.getNumNodes()
        # check if we have nodes
        if numNodes == 0:
            return None

        nextIdx = self.getCurrNodeIdx() + 1
        if nextIdx >= numNodes:
            nextIdx = 0
        self.setCurrNodeIdx(nextIdx)
        return self.getNodeByIdx(nextIdx)

    def getRerouteNode(self):
        node = self.getNextNode()
        while node != None:
            if node.isAlive():
                break
            self.removeNode(node.url) # remove dead node
            node = self.getNextNode()
        return node