from sense_hat import SenseHat, ACTION_PRESSED
import time


def clamp(n, _min=0, _max=7):
    return max(_min, min(n, _max))


def valid_position_index(n):
    return 0 <= n <= 7


class Transform:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

    def is_collided_with(self, transform):
        return self.get_position() == transform.get_position()


class Player(Transform):
    def __init__(self, _id=200, x=0, y=0):
        super().__init__(x, y)
        self._id = _id
        self.bombs = []
        self.explosions = []
        self.is_dead = False

    def move(self, x, y):
        self.x = clamp(self.x + x)
        self.y = clamp(self.y + y)

    def place_bomb(self):
        for bomb in self.bombs:
            if self.is_collided_with(bomb):
                return
        self.bombs.append(Bomb(self.x, self.y, self))
        pass

    def handle_bombs(self):
        bombs = self.bombs[:]
        for bomb in bombs:
            if bomb.should_explode():
                bomb.explode()

    def get_exploded_tiles(self):
        return set((x, y) for explosion in self.explosions for x, y in explosion.exploded_tiles)

    def handle_explosion(self):
        explosions = self.explosions[:]
        for explosion in explosions:
            if explosion.should_end():
                explosion.end()
        exploding_tiles = self.get_exploded_tiles()
        for x, y in exploding_tiles:
            for bomb in self.bombs:
                if x == bomb.x and y == bomb.y:
                    bomb.is_triggered = True
                    continue


class Bomb(Transform):
    def __init__(self, x, y, player, lifetime=2):
        super().__init__(x, y)
        self.player = player
        self.is_triggered = False
        self.explode_time = time.time() + lifetime

    def should_explode(self):
        return self.is_triggered or time.time() > self.explode_time

    def explode(self):
        player.bombs.remove(self)
        player.explosions.append(Explosion(self.x, self.y, self.player))


def get_exploded_tiles(x, y, length):
    tiles = []
    for i in range(-length, length + 1):
        if valid_position_index(y + i):
            tiles.append((x, y + i))
    for i in range(-length, length + 1):
        if valid_position_index(x + i):
            tiles.append((x + i, y))
    return set(tiles)


class Explosion:
    def __init__(self, x, y, player, length=2, lifetime=0.1):
        self.player = player
        self.end_time = time.time() + lifetime
        self.exploded_tiles = get_exploded_tiles(x, y, length)

    def should_end(self):
        return time.time() > self.end_time

    def end(self):
        player.explosions.remove(self)


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
    for x, y in player.get_exploded_tiles():
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
