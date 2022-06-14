import pyxel
import math

bullet_list = []
e_bullet_list = []
e_knife_list = []

class Bullet:
    def __init__(self, x, y, angle, radius, color, speed):
        self.x = x
        self.y = y
        self.angle = math.radians(angle)
        self.radius = radius
        self.color = color
        self.speed = speed
        self.alive = True

        bullet_list.append(self)

    def update(self):
        if (
            self.y < 0
            or self.y > pyxel.height
            or self.x < 0
            or self.x > pyxel.width
        ):
            self.alive = False

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, self.color)


class E_Bullet(Bullet):
    def __init__(self, x, y, angle, radius, color, speed):
        self.x = x
        self.y = y
        self.angle = math.radians(angle)
        self.radius = radius
        self.color = color
        self.speed = speed
        self.alive = True

        e_bullet_list.append(self)


class Player_n_way(Bullet):
    def __init__(self, x, y, angle, radius, color, speed, n):
        self.n = n
        super().__init__(x, y, angle, radius, color, speed)

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y -= math.sin(self.angle) * self.speed
        super().update()


def player_n_way(x, y, angle, radius, color, speed, n):
    for i in range(n):
        a = 90 - angle * (math.floor(n/2)-i)
        if n % 2 == 1:
            Player_n_way(x, y, a, radius, color, speed, n)


class Enemy_n_way(E_Bullet):
    def __init__(self, x, y, angle, radius, color, speed, n):
        self.n = n
        super().__init__(x, y, angle, radius, color, speed)

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        super().update()

    
def enemy_n_way(x, y, angle, radius, color, speed, n):
    for i in range(n):
        a = 90 - angle * (math.floor(n/2)-i)
        if n % 2 == 1:
            Enemy_n_way(x, y, a, radius, color, speed, n)


class Knife:
    def __init__(self, x, y, w, h, color, speed):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.speed = speed
        self.alive = True

        e_knife_list.append(self)

    def update(self):
        if (
            self.y < 0
            or self.y > pyxel.height
            or self.x < 0
            or self.x > pyxel.width - self.w
        ):
            self.alive = False

        self.y += self.speed

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, self.color)


def knife_shot(x, y, w, h, color, speed, n):
    dis = 6
    a = x - dis
    if n % 2 == 0:
        pass
    else:
        for i in range(n):   
            Knife(a, y, w, h, color, speed)
            a += dis