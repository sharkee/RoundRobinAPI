import requests
import sys
from concurrent.futures import ThreadPoolExecutor

from datetime import datetime
from router.constants import *

MAX_POST_TEST = 5000
MAX_THREADS = 1000

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
    print(resultObj)
    return resultObj

# retrieve initial values from server
initPostServerCount = 0
response = requests.post(ROUTER_SERVER + INFO_NODE_API, data="")
if response.status_code == 200:
    # retrieve post count from server
    res = response.json()
    for obj in res:
        initPostServerCount += obj['numPosts']
else:
    print(f"UNABLE TO RETRIEVE INFO FROM SERVER: {response.status_code}")
    sys.exit()

# create threadpool
with ThreadPoolExecutor(max_workers = MAX_THREADS) as executor:
    results = executor.map(postTest, range(MAX_POST_TEST))

# check individual post response
numOKPosts = 0
numERRPosts = 0
for rsp in results:
    if rsp["status"]  == 200:
        numOKPosts += 1
    else:
        numERRPosts += 1

print(f"Total OK Post Response: {numOKPosts}")
print(f"Total ERR Post Response: {numERRPosts}")

if numOKPosts == MAX_POST_TEST:
    print("POST RESPONSE TEST = [SUCCESS]")
else:
    print("POST RESPONSE TEST = [FAILED]")
    
response = requests.post(ROUTER_SERVER + INFO_NODE_API, data="")
if response.status_code == 200:
    # retrieve post count from server
    res = response.json()
    numPosts = 0
    for obj in res:
        print(f"Node({obj['url']}): {obj['numPosts']}")
        print(f"    Min Ave: {obj['minAverage']} ({obj['numPostsAtMin']})")
        print(f"    Max Ave: {obj['maxAverage']} ({obj['numPostsAtMax']})")
        print(f"    Custom: {obj['custom']}")
        numPosts += obj['numPosts']
    print(f"Total Posts Processed by Server Pre-Test: {initPostServerCount}")
    print(f"Total Posts Processed by Server Post-Test: {numPosts}")

    if numPosts == MAX_POST_TEST + initPostServerCount:
        print("POST SERVER TOTAL COUNT TEST = [SUCCESS]")
    else:
        print("POST SERVER TOTAL COUNT TEST = [FAILED]")
else:
    print(f"UNABLE TO RETRIEVE INFO FROM SERVER: {response.status_code}")