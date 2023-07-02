import atexit
import sys

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, abort
from flask_cors import CORS
from router.constants import *
from router.iw_round_robin_router import IWRoundRobinRouter

app = Flask(__name__)
CORS(app)
router = None

@app.route(POST_MESSAGE_API, methods=['POST'])
def handlePost():
    if request.is_json:
        response = router.rerouteMessage(request.get_json())
        if response != None:
            return response.json(), response.status_code
        abort(503) # no app nodes connected
    else:
        abort(400)

@app.route(CONNECT_NODE_API, methods=['POST'])
def handleNodeConnect():
    if request.is_json:
        return router.processNodeConnect(request.get_json())
    else:
        abort(400)
        
@app.route(DISCONNECT_NODE_API, methods=['POST'])
def handleNodeDisconnect():
    if request.is_json:
        return router.processNodeDisconnect(request.get_json())
    else:
        abort(400)
        
@app.route(HEARTBEAT_NODE_API, methods=['POST'])
def handleNodeHeartbeat():
    if request.is_json:
        return router.processNodeHeartbeat(request.get_json())
    else:
        abort(400)

@app.route(INFO_NODE_API, methods=['POST'])
def handleInfo():
    return router.processInfo()

if __name__ == '__main__':
    router = IWRoundRobinRouter()
    
    # schedule dead node removal task
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=router.removeDeadNodes, trigger="interval", seconds=DEADNODE_REMOVAL_INTERVAL)
    scheduler.start()
    
    # stop scheduled tasks
    atexit.register(lambda: scheduler.shutdown())
    
    app.run(host=ROUTER_HOST, port=ROUTER_PORT, threaded=True)