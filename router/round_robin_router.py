from router.router import Router

class RoundRobinRouter(Router):
    currNodeIdx = -1
        
    def removeNode(self, url):
        for idx, node in enumerate(self.nodeTable):
            if url == node.url:
                del self.nodeTable[idx]
                # update index tracker when necessary
                if self.currNodeIdx >= idx:
                    self.currNodeIdx - 1
                break
        return

    def getNextNode(self):
        numNodes = len(self.nodeTable)
        if numNodes == 0:
            return None
    
        nextIdx = self.currNodeIdx + 1
        if nextIdx < numNodes:
            self.currNodeIdx = nextIdx
        else:
            self.currNodeIdx = 0
        return self.nodeTable[self.currNodeIdx]
        
    def getRerouteNode(self):
        node = self.getNextNode()
        while node != None:
            if node.isAlive():
                break;
            self.removeNode(node.url) # remove dead node
            node = self.getNextNode()
        return node;