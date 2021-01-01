from sense_hat import SenseHat, ACTION_PRESSED
import time


def clamp(n, _min=0, _max=7):
    return max(_min, min(n, _max))


def valid_position_index(n):
    return 0 <= n <= 7


class Transform:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def get_position(self):
        return self.x, self.y

    def is_collided_with(self, transform):
        return self.get_position() == transform.get_position()


class Player(Transform):
    def __init__(self, _id=200, x=0, y=0, color = (0, 255, 0)):
        super().__init__(x, y, color)
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

    def handle_explosions(self):
        explosions = self.explosions[:]
        for explosion in explosions:
            if explosion.should_end():
                explosion.end()
            for bomb in self.bombs:
                if explosion.is_collided_with(bomb):
                    bomb.is_triggered = True


class Bomb(Transform):
    def __init__(self, x, y , player, lifetime=2, length=2, color = (255, 0, 0)):
        super().__init__(x, y, color)
        self.player = player
        self.is_triggered = False
        self.length = length
        self.explode_time = time.time() + lifetime

    def should_explode(self):
        return self.is_triggered or time.time() > self.explode_time

    def explode(self):
        player.bombs.remove(self)
        player.explosions.extend(self.get_explosions())

    def get_explosions(self):
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
        return [Explosion(tile[0], tile[1], self.player) for tile in set(tiles)]


class Explosion(Transform):
    def __init__(self, x, y, player, lifetime=0.1, color = (255, 0, 255)):
        super().__init__(x, y, color)
        self.player = player
        self.end_time = time.time() + lifetime

    def should_end(self):
        return time.time() > self.end_time

    def end(self):
        player.explosions.remove(self)


sense = SenseHat()
sense.clear()



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
    sense.set_pixel(player.x, player.y, player.color)


def render_bombs():
    for bomb in player.bombs:
        sense.set_pixel(bomb.x, bomb.y, bomb.color)


def render_explosions():
    for explosion in player.explosions:
        sense.set_pixel(explosion.x, explosion.y, explosion.color)


def update():
    sense.clear()
    render_player()
    player.handle_bombs()
    render_bombs()
    player.handle_explosions()
    render_explosions()


sense.stick.direction_up = move_up
sense.stick.direction_down = move_down
sense.stick.direction_left = move_left
sense.stick.direction_right = move_right
sense.stick.direction_middle = place_bomb
while True:
    update()
