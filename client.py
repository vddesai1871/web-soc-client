import socketio
import urllib.request
import redis
import json

sio = socketio.Client(logger=True)

class MyCustomNamespace(socketio.ClientNamespace):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_my_event(self, data):
        self.emit('my_response', data)

    def on_update(self, data):
        print("UPDATED: ")
        print(data)

sio.register_namespace(MyCustomNamespace('/test'))
sio.connect("http://localhost:8080/serverapi")
sio.emit("my_event", {"message": "Hey, Hii"})
con = redis.StrictRedis(host="localhost", port=6379, db=0)

def get_objects(url):
    resp = urllib.request.urlopen(url)
    data = json.loads(resp.read().decode('utf-8'))
    print("Cached ")
    print(data)
    con.set("cache", json.dumps(data))
    d = con.get("cache").decode('utf-8')
    print("Got ")
    print(d)


get_objects("http://localhost:8080/serverapi/DroneCollection")