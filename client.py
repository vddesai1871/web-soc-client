import socketio
import urllib.request
import redis
import json

sio = socketio.Client(logger=True)


def update_obj(id, obj):
    con.set(obj["@type"]+":"+id, json.dumps(obj))


class MyCustomNamespace(socketio.ClientNamespace):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_update(self, data):
        print("UPDATED: ")
        print("ID")
        print(data["id"])
        print(data["obj"])
        update_obj(data["id"], data["obj"])


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
    for obj in data["members"]:
        id = obj["@id"].split('/')[-1]
        obj_type = obj["@type"]
        res = urllib.request.urlopen(url+"/"+id)
        member_obj = json.loads(res.read().decode('utf-8'))
        member_obj.pop("@context")
        member_obj.pop("@id")
        con.set(obj_type+":"+id, json.dumps(member_obj))
        tmp = con.get(obj_type+":"+id).decode('utf-8')
        print(tmp)
    con.set("cache", json.dumps(data))
    d = con.get("cache").decode('utf-8')
    print("Got from cache ")
    print(d)


get_objects("http://localhost:8080/serverapi/DroneCollection")
sio.emit("my_event", {"message": "Hey, Hii"}, namespace="/test")