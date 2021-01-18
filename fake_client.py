import socketio

sio = socketio.Client()
URL = 'https://bomberrypi.herokuapp.com/socket.io'


@sio.event
def connect():
    print("Connect to server")
    sio.emit('matchmaking')


@sio.event()
def start_game(pos):
    print(pos)


sio.connect(URL)
