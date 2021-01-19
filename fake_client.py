import socketio
import keyboard

sio = socketio.Client()
URL = 'https://bomberrypi.herokuapp.com/'


def clamp(n, _min=0, _max=7):
    return max(_min, min(n, _max))


class Player:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def move(self, x, y):
        next_position = clamp(self.x + x), clamp(self.y + y)
        self.x, self.y = next_position

    def get_position_packet(self):
        return {'x': self.x, 'y': self.y}


@sio.event
def connect():
    print("Connect to server")
    sio.emit('matchmaking')


@sio.event()
def start_game(pos):
    print(pos)
    player = Player(pos['x1'], pos['y1'])
    while True:
        if keyboard.is_pressed('a'):
            player.move(-1, 0)
            sio.emit('move', player.get_position_packet())
        if keyboard.is_pressed('d'):
            player.move(1, 0)
            sio.emit('move', player.get_position_packet())
        if keyboard.is_pressed('w'):
            player.move(0, -1)
            sio.emit('move', player.get_position_packet())
        if keyboard.is_pressed('s'):
            player.move(0, 1)
            sio.emit('move', player.get_position_packet())
        if keyboard.is_pressed('j'):
            sio.emit('place_bomb')


@sio.event()
def move(pos):
    print(pos)


sio.connect(URL)
