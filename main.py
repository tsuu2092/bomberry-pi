from sense_hat import SenseHat, ACTION_PRESSED
import time


def clamp(n, _min=0, _max=7):
    return max(_min, min(n, _max))


def valid_position_index(n):
    return 0 <= n <= 7


class Explosion:
    def __init__(self, x, y, player, length=2, lifetime=0.1):
        self.x = x
        self.y = y
        self.player = player
        self.length = length
        self.end_time = time.time() + lifetime

    def should_end(self):
        return time.time() > self.end_time

    def end(self):
        player.explosions.remove(self)

    def get_exploded_tiles(self):
        tiles = []
        x = self.x
        y = self.y
        length = self.length
        for i in range(-length, length + 1):
            if valid_position_index(y + i):
                tiles.append((x, y + i))
        for i in range(-length, length + 1):
            if valid_position_index(x + i):
                tiles.append((x + i, y))
        return list(set(tiles))


class Player:
    def __init__(self):
        self.id = 200
        self.x = 0
        self.y = 0
        self.bombs = []
        self.explosions = []
        self.is_dead = False

    def move(self, x, y):
        self.x = clamp(self.x + x)
        self.y = clamp(self.y + y)

    def place_bomb(self):
        self.bombs.append(Bomb(self.x, self.y, self))
        pass

    def handle_bombs(self):
        bombs = self.bombs[:]
        for bomb in bombs:
            if bomb.should_explode():
                self.explosions.append(bomb.explode())

    def get_exploding_tiles(self):
        return set((x, y) for explosion in self.explosions for x, y in explosion.get_exploded_tiles())

    def handle_explosion(self):
        explosions = self.explosions[:]
        for explosion in explosions:
            if explosion.should_end():
                explosion.end()
        exploding_tiles = self.get_exploding_tiles()
        for x, y in exploding_tiles:
            for bomb in self.bombs:
                if x == bomb.x and y == bomb.y:
                    bomb.is_triggered = True
                    continue


class Bomb:
    def __init__(self, x, y, player, lifetime=2):
        self.x = x
        self.y = y
        self.player = player
        self.is_triggered = False
        self.explode_time = time.time() + lifetime

    def should_explode(self):
        return self.is_triggered or time.time() > self.explode_time

    def explode(self):
        player.bombs.remove(self)
        return Explosion(self.x, self.y, player)


sense = SenseHat()
sense.clear()

player_color = (255, 0, 0)
bomb_color = (0, 255, 0)
explosion_color = (0, 0, 255)
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


def render_explosion():
    for explosion in player.explosions:
        for x, y in explosion.get_exploded_tiles():
            sense.set_pixel(x, y, explosion_color)


def update():
    sense.clear()
    render_player()
    player.handle_bombs()
    render_bombs()
    player.handle_explosion()
    render_explosion()


sense.stick.direction_up = move_up
sense.stick.direction_down = move_down
sense.stick.direction_left = move_left
sense.stick.direction_right = move_right
sense.stick.direction_middle = place_bomb
while True:
    update()
