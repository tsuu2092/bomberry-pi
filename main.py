from sense_hat import SenseHat, ACTION_PRESSED
import time


def clamp(n, _min=0, _max=7):
    return max(_min, min(n, _max))


def valid_position_index(n):
    return 0 <= n <= 7


class Map():
    player_color = (0, 125, 0)
    player_bomb_color = (0, 255, 255)
    player_explosion_color = (0, 0, 255)
    enemy_color = (125, 0, 0)
    enemy_bomb_color = (255, 0, 0)
    enemy_explosion_color = (255, 255, 0)

    def __init__(self, sense, player, enemy):
        self.is_playing = True
        self.sense = sense
        self.player = player
        self.enemy = enemy
        self.enemy.place_bomb()
        self.clear()

    def clear(self):
        self.sense.clear()

    def render(self, color, *transforms):
        for transform in transforms:
            self.sense.set_pixel(transform.x, transform.y, color)

    def render_all(self):
        self.clear()
        self.render(self.__class__.player_color, self.player)
        self.render(self.__class__.player_bomb_color, *self.player.bombs)
        self.render(self.__class__.player_explosion_color, *self.player.explosions)
        self.render(self.__class__.enemy_color, self.enemy)
        self.render(self.__class__.enemy_bomb_color, *self.enemy.bombs)
        self.render(self.__class__.enemy_explosion_color, *self.enemy.explosions)

    def handle_all(self):
        self.player.handle_bombs()
        self.enemy.handle_bombs()
        self.player.handle_explosions()
        self.enemy.handle_explosions()
        self.player.invalid_positions = self.enemy.get_collider_positions()
        self.player.dead_positions = self.enemy.get_explosion_positions()
        self.enemy.invalid_positions = self.player.get_collider_positions()
        self.enemy.dead_positions = self.player.get_explosion_positions()
        if self.player.is_hit():
            self.sense.show_message("You lose")
            return
        if self.enemy.is_hit():
            self.sense.show_message("You win")
            return

    def update(self):
        self.handle_all()
        self.render_all()


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
        self.invalid_positions = []
        self.dead_positions = []

    def get_collider_positions(self):
        return set([self.get_position()] + [bomb.get_position() for bomb in self.bombs])

    def get_explosion_positions(self):
        return set(explosion.get_position() for explosion in self.explosions)

    def is_hit(self):
        return self.get_position() in self.dead_positions

    def move(self, x, y):
        next_position = clamp(self.x + x), clamp(self.y + y)
        if next_position in self.invalid_positions:
            return
        self.x, self.y = next_position

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
    def __init__(self, x, y, player, lifetime=2, length=2, ):
        super().__init__(x, y)
        self.player = player
        self.is_triggered = False
        self.length = length
        self.explode_time = time.time() + lifetime

    def should_explode(self):
        return self.is_triggered or time.time() > self.explode_time

    def explode(self):
        self.player.bombs.remove(self)
        self.player.explosions.extend(self.get_explosions())

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
    def __init__(self, x, y, player, lifetime=0.1):
        super().__init__(x, y)
        self.player = player
        self.end_time = time.time() + lifetime

    def should_end(self):
        return time.time() > self.end_time

    def end(self):
        self.player.explosions.remove(self)


sense = SenseHat()
sense.clear()

player = Player()
enemy = Player(300, 2, 2)
_map = Map(sense, player, enemy)


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


sense.stick.direction_up = move_up
sense.stick.direction_down = move_down
sense.stick.direction_left = move_left
sense.stick.direction_right = move_right
sense.stick.direction_middle = place_bomb

while True:
    _map.update()
