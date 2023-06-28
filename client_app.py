import atexit
import sys
import time

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request
from flask_cors import CORS
from router.constants import *
from router.router_client import RouterClient

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def handle_post():
    if request.is_json:
        return request.json
    else:
        return "Content type is not supported"

if __name__ == '__main__':
    # default values
    p = 5000
    h = "localhost"
    
    # override via arguments
    n = len(sys.argv) 
    if n == 2:
        p = int(sys.argv[1])
    elif n == 3:
        h = sys.argv[1]
        p = int(sys.argv[2])

    # setup router client
    myUrl = f"http://{h}:{p}"
    routerClient = RouterClient(myUrl, ROUTER_SERVER)
    
    # connect to router
    response = routerClient.connect()
    isOK = (response.status_code == 200 or response.status_code == 201)
    if(not isOK):
        print(f"Connect to router server({ROUTER_SERVER}) returned code {response.status_code}")
        exit()
    
    # schedule heartbeat
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=routerClient.sendHeartbeat, trigger="interval", seconds=HEARTBEAT_INTERVAL)
    scheduler.start()
    
    # stop sending heartbeat at exit
    atexit.register(lambda: scheduler.shutdown())
    
    # send disconnect message at exit
    atexit.register(lambda: routerClient.disconnect())

    # run the webapp
    app.run(host=h, port=p)