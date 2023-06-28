import sys

from flask import Flask, request, abort
from flask_cors import CORS
from router.constants import *
from router.round_robin_router import RoundRobinRouter

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

if __name__ == '__main__':
    router = RoundRobinRouter()
    app.run(host=ROUTER_HOST, port=ROUTER_PORT)