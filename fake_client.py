import socketio

sio = socketio.Client()
URL = 'https://bomberrypi.herokuapp.com/socket.io'


@sio.event
def connect():
    sio.emit('matchmaking')


@sio.event()
def start_game(pos):
    print(pos)


sio.connect(URL)
