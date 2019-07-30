import socketio
import urllib.request
import redis
import json
import time

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

    def on_my_response(self, data):
        print("Got response")
        self.emit('resp', data)
    
    def on_modification_table_diff(self, data):
        print("Modification Table Diff:")
        print(data)


sio.register_namespace(MyCustomNamespace('/sync'))
sio.connect("http://localhost:8080/serverapi")
sio.emit("my_event", {"message": "Hey, Hii"}, namespace="/sync")
time.sleep(10)
sio.emit("get_modification_table_diff", {"agent_job_id": "7bb5c816-4436-4ee8-8aaf-36017ae16e59"}, namespace = "/sync")
