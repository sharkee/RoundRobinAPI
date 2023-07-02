# Router Constants

# in seconds
HEARTBEAT_INTERVAL = 5

# maximum wait time until considered as disconnected
# * in seconds
HEARTBEAT_MAX_LIFE = 10

# router APIs
POST_MESSAGE_API = "/"
CONNECT_NODE_API = "/connect"
DISCONNECT_NODE_API = "/disconnect"
HEARTBEAT_NODE_API = "/heartbeat"
INFO_NODE_API = "/info"

# router server URL
ROUTER_SERVER = "http://localhost:5000"
ROUTER_HOST = "localhost"
ROUTER_PORT = 5000