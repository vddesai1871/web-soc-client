import socketio

sio = socketio.Client(logger=True)

class MyCustomNamespace(socketio.ClientNamespace):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_my_event(self, data):
        self.emit('my_response', data)

    def on_update(self, data):
        print(data)

sio.register_namespace(MyCustomNamespace('/test'))
sio.connect("http://localhost:8080/serverapi")
sio.emit("my_event", {"message": "Hey, Hii"})
