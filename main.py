from sense_hat import SenseHat, ACTION_PRESSED
import time


def clamp(n, _min=0, _max=7):
    return max(_min, min(n, _max))


class Explosion:
    def __init__(self, x, y, length=1):
        self.x = x
        self.y = y
        self.length = length


class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.explode_time = time.time() + 1

    def explode(self):
        pass


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.bombs = []
        self.is_dead = False

    def move(self, x, y):
        self.x = clamp(self.x + x)
        self.y = clamp(self.y + y)

    def place_bomb(self):
        self.bombs.append(Bomb(self.x, self.y))
        pass

    def handle_bomb_explosion(self):
        bombs = self.bombs[:]
        current_time = time.time()
        for bomb in bombs:
            if current_time > bomb.explode_time:
                bomb.explode()
                self.bombs.remove(bomb)


sense = SenseHat()
sense.clear()

player_color = (255, 0, 0)
bomb_color = (0, 255, 0)
player = Player()


def move_up(event):
    if event.action == ACTION_PRESSED:
        player.move(0, -1)


def move_down(event):
    if event.action == ACTION_PRESSED:
        player.move(0, 1)


def move_left(event):
    if event.action == ACTION_PRESSED:
        player.move(-1, 0)


def move_right(event):
    if event.action == ACTION_PRESSED:
        player.move(1, 0)


def place_bomb(event):
    if event.action == ACTION_PRESSED:
        player.place_bomb()


def render_player():
    sense.set_pixel(player.x, player.y, player_color)


def render_bombs():
    for bomb in player.bombs:
        sense.set_pixel(bomb.x, bomb.y, bomb_color)


def update():
    sense.clear()
    render_player()
    player.handle_bomb_explosion()
    render_bombs()


sense.stick.direction_up = move_up
sense.stick.direction_down = move_down
sense.stick.direction_left = move_left
sense.stick.direction_right = move_right
sense.stick.direction_middle = place_bomb

while True:
    update()
