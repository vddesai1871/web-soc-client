import socketio
import urllib.request
import redis
import json

sio = socketio.Client(logger=True)


def update_obj(id, obj):
    con.set(obj["@type"]+":"+id, json.dumps(obj))


class MyCustomNamespace(socketio.ClientNamespace):
    def on_connect(self):
        print("Connected")

    def on_disconnect(self):
        pass

    def on_update(self, data):
        print("UPDATED: ")
        print("ID")
        print(data["new_job_id"])
        print(data["last_job_id"])
        print(data["method"])
        print(data["resource_url"])

    def on_my_response(self, data):
        print("Got response")
        self.emit('resp', data)


sio.register_namespace(MyCustomNamespace('/sync'))
sio.connect("http://localhost:8080/serverapi")
sio.emit("my_event", {"message": "Hey, Hii"}, namespace="/sync")
