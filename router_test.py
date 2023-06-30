import requests
import threading

from datetime import datetime
from router.constants import *

results = []

# decorator to ensure thread safety
def synchronized(func):
    func.__lock__ = threading.Lock()
    def syncedFunc(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)
    return syncedFunc

@synchronized
def appendResult(result):
    global results
    results.append(result)
    print(result)

def postTest(value):
    jsonObj = {
        "test":"cmd",
        "data":value
    }
    resultObj = {
        "duration":0,
        "value":value,
        "status":0,
        "response":""
    }
    start = datetime.now()
    response = requests.post(ROUTER_SERVER + POST_MESSAGE_API, json=jsonObj)
    end = datetime.now()
    resultObj["duration"] = (end - start).total_seconds() * 1000
    resultObj["status"] = response.status_code
    resultObj["response"] = response.text
    appendResult(resultObj)
    
MAX_POST_TEST = 1000
threadList = []

for i in range(MAX_POST_TEST):
    thread = threading.Thread(target=postTest, args=[i])
    threadList.append(thread)

for thread in threadList:
    thread.start()
    
for thread in threadList:
    thread.join()
    thread = threading.Thread(target=postTest, args=[i])
    
# print(results)