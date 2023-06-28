# HTTP Round Robin API
Description:
Round Robin API which receives HTTP POSTS and routes them to one of a list of Application APIs

## Requirements:
* Python 3.8.3 (https://www.python.org/downloads/)
* Flask 2.3.2
```
pip install Flask
```
* Flask-Cors 4.0.0
```
pip install flask-cors
```
* APScheduler 3.10.1
```
pip install APScheduler
```

## Running 
* Router Server App:
```
python router_app.py
```
* Router Client App:
```
python client_app.py <host name> <port>
```
* Test Web App: just open test/app_test.html using a web browser
