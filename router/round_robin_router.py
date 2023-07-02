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
    def incrementCurrNodeIdx(self):
        nextIdx = self.currNodeIdx + 1
        if nextIdx >= self.getNumNodes():
            nextIdx = 0
        self.currNodeIdx = nextIdx
        return nextIdx
    
    @synchronized_with_attr("currNodeIdxLock")
    def removeNode(self, url):
        idx = super().removeNode(url)
        if idx >= 0:
            # update index tracker when necessary
            if self.currNodeIdx >= idx:
                self.currNodeIdx -= 1
        return idx

    @synchronized_with_attr("nodeTablelock")
    def getRerouteNode(self):
        numNodes = self.getNumNodes()
        # check if we have nodes
        if numNodes == 0:
            return None

        return self.getNodeByIdx(self.incrementCurrNodeIdx())