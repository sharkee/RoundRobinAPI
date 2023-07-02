import threading
from router.round_robin_router import RoundRobinRouter
from router.synchronized import synchronized_with_attr

# Implementation of an interleaved weighted round robin where the weights are 
# dynamically updated based on node performance
class IWRoundRobinRouter(RoundRobinRouter):
    MAX_START_WEIGHT = 10
    MIN_WEIGHT = 1
    
    # weights of each node
    maxWeights = []
    weights = []
    weightsLock = threading.RLock()
    
    @synchronized_with_attr("weightsLock")
    def addNode(self, url):
        super().addNode(url) # this is already synchronized
        self.weights.append(self.MAX_START_WEIGHT)
        self.maxWeights.append(self.MAX_START_WEIGHT)
        
    @synchronized_with_attr("weightsLock")
    def removeNode(self, url):
        idx = super().removeNode(url)
        if idx >= 0:
            del self.weights[idx]
            del self.maxWeights[idx]
        return idx
    
    @synchronized_with_attr("weightsLock")
    def getWeight(self, idx):
        return self.weights[idx]
        
    @synchronized_with_attr("weightsLock")
    def setWeight(self, idx, value):
        self.weights[idx] = value
        
    @synchronized_with_attr("weightsLock")
    def getMaxWeight(self, idx):
        return self.maxWeights[idx]
        
    @synchronized_with_attr("weightsLock")
    def setMaxWeight(self, idx, value):
        self.maxWeights[idx] = value
        
    # check weights and reset if necessary
    @synchronized_with_attr("weightsLock")
    def checkWeights(self):
        for weight in self.weights:
            if weight > 0:
                return
        # reset if all weights are 0
        self.weights[:] = [maxWeight for maxWeight in self.maxWeights]

    @synchronized_with_attr("weightsLock")
    def checkPerformance(self):
        # check performance of all nodes
        for idx, node in enumerate(self.nodeTable):
            if node.numPosts % 10:
                diff = node.averagePostTime_last10 - node.minAverage
                # node is, at least, 50% slower than it's minimum average
                # if diff >= (node.minAverage * 0.5):
                if diff >= 25:
                    # set max weight to half
                    maxWeight = self.getMaxWeight(idx)
                    maxWeight = maxWeight // 2
                    if maxWeight < self.MIN_WEIGHT:
                        maxWeight = self.MIN_WEIGHT
                    self.setMaxWeight(idx, maxWeight)
    
    @synchronized_with_attr("weightsLock")
    def processInfo(self):
        result = super().processInfo()
        for idx in range(len(result)):
            print(result[idx])
            result[idx]['custom'] = {
                "maxWeight" : self.getMaxWeight(idx)
            }
        return result
        
    @synchronized_with_attr("nodeTablelock")
    def getRerouteNode(self):
        numNodes = self.getNumNodes()
        # check if we have nodes
        if numNodes == 0:
            return None

        self.checkPerformance()
        self.checkWeights()
        
        # check if current node is available based on current weight
        currIdx = self.incrementCurrNodeIdx()
        currWeight = self.getWeight(currIdx)
        if currWeight > 0:
            # weight > 0 means it's available
            self.setWeight(currIdx, currWeight - 1)
            return self.getNodeByIdx(self.getCurrNodeIdx())
        
        # find next available node based on current weight
        startIdx = currIdx # startIdx to prevent infinite loop
        currIdx = self.incrementCurrNodeIdx()
        while startIdx != currIdx:
            currWeight = self.getWeight(currIdx)
            if currWeight > 0:
                self.setWeight(currIdx, currWeight - 1)
                return self.getNodeByIdx(self.getCurrNodeIdx())
            currIdx = self.incrementCurrNodeIdx()
        
        # self.checkWeights should prevent this from happening
        return None