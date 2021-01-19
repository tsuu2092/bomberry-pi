import socketio

sio = socketio.Client()
URL = 'https://bomberrypi.herokuapp.com/'


@sio.event
def connect():
    print("Connect to server")
    sio.emit('matchmaking')


@sio.event()
def start_game(pos):
    print(pos)
    while True:
        x, y = map(int, input("Your move: ").split())
        sio.emit('move', {'x': x, 'y': y})


sio.connect(URL)
