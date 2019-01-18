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

    def on_update(self, data):
        print("UPDATED: ")
        print(data)

    def on_my_response(self, data):
        print("Got response")
        self.emit('resp', data)


sio.register_namespace(MyCustomNamespace('/test'))
sio.connect("http://localhost:8080/serverapi")
con = redis.StrictRedis(host="localhost", port=6379, db=0)

def get_objects(url):
    resp = urllib.request.urlopen(url)
    print(resp)
    data = json.loads(resp.read().decode('utf-8'))
    print("Cached ")
    print(data)
    con.set("cache", json.dumps(data))
    d = con.get("cache").decode('utf-8')
    print("Got from cache ")
    print(d)


get_objects("http://localhost:8080/serverapi/DroneCollection")
sio.emit("my_event", {"message": "Hey, Hii"}, namespace="/test")