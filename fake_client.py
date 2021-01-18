import socketio

sio = socketio.Client()
URL = 'https://bomberrypi.herokuapp.com/'


@sio.event
def connect():
    sio.emit('matchmaking')


sio.connect(URL)
