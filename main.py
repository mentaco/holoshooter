from math import fabs
from random import random, uniform
from numpy import ERR_LOG
import pyxel
import danmaku

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2

STAR_COUNT = 100
STAR_COLOR_HIGH = 12
STAR_COLOR_LOW = 5

PLAYER_WIDTH = 16
PLAYER_HEIGHT = 16
PLAYER_SPEED = 1
PLAYER_HP = 3

JUDGE_RADIUS = 1.3

ENEMY_WIDTH = 16
ENEMY_HEIGHT = 16

BULLET_RADIUS = 1
BULLET_COLOR = 7
BULLET_SPEED = 2.5
BULLET_INTERVAL = 12
BULLET_ANGLE = 5

KNIFE_WIDTH = 1.6
KNIFE_HEIGHT = 2

BLAST_START_RADIUS = 1
BLAST_END_RADIUS = 8
BLAST_COLOR_IN = 7
BLAST_COLOR_OUT = 10

bullet_list = danmaku.bullet_list
e_bullet_list = danmaku.e_bullet_list
e_knife_list = danmaku.e_knife_list
enemy_list = []
blast_list = []


def update_list(list):
    for elem in list:
        elem.update()

def draw_list(list):
    for elem in list:
        elem.draw()

def cleanup_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if elem.alive == False:
            list.pop(i)
        else:
            i += 1


class Background:
    def __init__(self):
        self.star_list = []
        for i in range(STAR_COUNT):
            self.star_list.append(
                (random() * pyxel.width, random() * pyxel.height, random())
            )

    def update(self):
        for i, (x, y, speed) in enumerate(self.star_list):
            y += speed
            if y >= pyxel.height:
                y -= pyxel.height
            self.star_list[i] = (x, y, speed)

    def draw(self):
        for (x, y, speed) in self.star_list:
            pyxel.pset(x, y, STAR_COLOR_HIGH if speed > 1.8 else STAR_COLOR_LOW)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = PLAYER_WIDTH
        self.h = PLAYER_HEIGHT
        self.hp = PLAYER_HP
        self.alive = True
        self.urv = False
        self.damage_count = 0
    
    def update(self):
        if pyxel.btn(pyxel.KEY_A):
            self.x -= PLAYER_SPEED

        if pyxel.btn(pyxel.KEY_D):
            self.x += PLAYER_SPEED

        if pyxel.btn(pyxel.KEY_W):
            self.y -= PLAYER_SPEED

        if pyxel.btn(pyxel.KEY_S):
            self.y += PLAYER_SPEED

        self.x = max(self.x, 0)
        self.x = min(self.x, pyxel.width - self.w)
        self.y = max(self.y, 0)
        self.y = min(self.y, pyxel.height - self.h)

        if pyxel.btnp(pyxel.KEY_SPACE, BULLET_INTERVAL, BULLET_INTERVAL):
            danmaku.player_n_way(self.x + self.w/2, self.y, BULLET_ANGLE, BULLET_RADIUS, BULLET_COLOR, BULLET_SPEED, 3)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 32, 16, self.w, self.h, 3)


class Judge:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = JUDGE_RADIUS
    
    def update(self, x, y):
        self.x = x
        self.y = y

    def draw(self, x, y):
        pyxel.circ(x, y, self.r, 7)

class Enemy:
    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.w = ENEMY_WIDTH
        self.h = ENEMY_HEIGHT
        self.hp = hp
        self.alive = True

        enemy_list.append(self)


class Coco(Enemy):
    def update(self):
        if 0 < pyxel.frame_count % 200 < 100:
            self.x += 0.4
        elif 100 < pyxel.frame_count % 200 < 200:
            self.x -= 0.4
        else:
            danmaku.enemy_n_way(self.x + self.w/2, self.y + self.h/2, 9, 1.8, 9, 0.5, 3)

        self.y += 0.2

        if self.y > pyxel.height:
            self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, self.w, self.h, 3)


class Shion(Enemy):
    def update(self):
        if 0 < pyxel.frame_count % 200 < 100:
            self.y += 0.6
        elif 100 < pyxel.frame_count % 200 < 200:
            self.y -= 0.6
        else:
            danmaku.enemy_n_way(self.x + self.w/2, self.y + self.h/2, 24, 2, 2, 0.4, 15)

        self.x += 0.8

        if self.x > pyxel.width:
            self.alive = False
        
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16, 0, self.w, self.h, 3)


class Kanata(Enemy):
    def update(self):
        if pyxel.frame_count % 200 < 100:
            self.x -= 0.7
        elif 100 < pyxel.frame_count % 200:
            self.x += 0.2
        else:
            danmaku.enemy_n_way(self.x + self.w/2, self.y + self.h/2, 40, 3, 6, 0.2, 9)

        if self.x < -ENEMY_WIDTH:
            self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 32, 0, self.w, self.h, 3)


class Rushia(Enemy):
    def update(self):
        self.x -= 0.8

        if pyxel.frame_count % 100 == 0:
            danmaku.knife_shot(self.x + 7.2, self.y + self.h, KNIFE_WIDTH, KNIFE_HEIGHT, 13, 1.5, 5)

        if self.x < -ENEMY_WIDTH:
            self.alive = False
        
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 48, 0, self.w, self.h, 14)


class Ayame(Enemy):
    def update(self):
        if 0 < pyxel.frame_count % 200 < 100:
            self.y += 0.3
        elif 100 < pyxel.frame_count % 200 < 200:
            self.y -= 0.3
        else:
            danmaku.enemy_n_way(self.x + self.w/2, self.y + self.h/2, 11, 1.5, 8, 1, 5)

        self.x += 0.6

        if self.x > pyxel.width:
            self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 16, self.w, self.h, 3)


class Choco(Enemy):
    def update(self):
        if 0 < pyxel.frame_count % 200 < 100:
            self.x += 0.6
        elif 100 < pyxel.frame_count % 200 < 200:
            self.x -= 0.6
        elif pyxel.frame_count % 200 == 100:
            danmaku.enemy_n_way(self.x + self.w/2, self.y + self.h/2, 40, 1.2, 10, 0.7, 9)
        else:
            danmaku.knife_shot(self.x + 7.2, self.y + self.h, KNIFE_WIDTH, KNIFE_HEIGHT, 13, 1.5, 3)

        self.y += 0.6

        if self.y > pyxel.height:
            self.alive = False
        
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16, 16, self.w, self.h, 3)



class Blast:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = BLAST_START_RADIUS
        self.alive = True

        blast_list.append(self)

    def update(self):
        self.radius += 1

        if self.radius > BLAST_END_RADIUS:
            self.alive = False

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, BLAST_COLOR_IN)
        pyxel.circb(self.x, self.y, self.radius, BLAST_COLOR_OUT)


class App:
    def __init__(self):
        pyxel.init(192, 256, title="Hololive", fps=120, quit_key=pyxel.KEY_Q)
        pyxel.load('holomem.pyxres')

        self.music_flug = False

        self.background = Background()

        self.scene = SCENE_TITLE
        self.score = 0
        self.player = Player(pyxel.width / 2 - 8, pyxel.height - 30)
        self.judge = Judge(self.player.x + PLAYER_WIDTH/2, self.player.y + PLAYER_HEIGHT/2)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.background.update()

        if self.scene == SCENE_TITLE:
            self.update_title_scene()

        elif self.scene == SCENE_PLAY:
            self.update_play_scene()

        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()

    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_PLAY

    def update_play_scene(self):
        if self.music_flug == False:
            pyxel.playm(1, loop=True)
            self.music_flug = True

        self.player.update()
        self.judge.update(self.player.x + PLAYER_WIDTH/2, self.player.y + PLAYER_HEIGHT/2)

        if pyxel.frame_count % 500 == 0:
            Coco(random() * pyxel.width, -ENEMY_HEIGHT, 6)
        elif pyxel.frame_count % 500 == 100:
            Shion(-ENEMY_WIDTH, uniform(0, 0.5) * pyxel.height, 3)
        elif pyxel.frame_count % 600 == 30:
            Kanata(pyxel.width, uniform(0, 0.8) * pyxel.height, 4)
        elif pyxel.frame_count % 600 == 100:
            Rushia(pyxel.width + ENEMY_WIDTH, uniform(0, 0.6) * pyxel.height, 5)
        elif pyxel.frame_count % 600 == 400:
            Ayame(-ENEMY_WIDTH, uniform(0, 0.5) * pyxel.height, 6)
        elif pyxel.frame_count % 700 == 350:
            Choco(uniform(0.3, 0.7) * pyxel.width, -ENEMY_HEIGHT, 4)

        for a in enemy_list:
            for b in bullet_list:
                if (
                    (a.x - BULLET_RADIUS <= b.x <= a.x and a.y <= b.y <= a.y + a.h)
                    or (a.x + a.w <= b.x <= a.x + a.w + BULLET_RADIUS and a.y <= b.y <= a.y + a.h)
                    or (a.x <= b.x <= a.x + a.w and a.y + a.h <= b.y <= a.y + a.h + BULLET_RADIUS)
                ):
                    b.alive = False
                    a.hp -= 1

                    if a.hp <= 0:
                        a.alive = False
                        Blast(a.x + a.w/2, a.y + a.h/2)
                        self.score += 30

        for c in e_bullet_list:
            if (
                (abs(self.judge.x-c.x) < self.judge.r + c.radius and abs(self.judge.y-c.y) < self.judge.r + c.radius)
                and self.player.urv == False
                ):
                c.alive = False
                self.player.hp -= 1
                Blast(self.player.x + self.player.w/2, self.player.y + self.player.h/2)

                if self.player.hp <= 0:
                    self.player.alive = False
                    self.scene = SCENE_GAMEOVER
                else:
                    self.player.urv = True

        for d in e_knife_list:
            if (
                (d.x - self.judge.r <= self.judge.x <= d.x and d.y <= self.judge.y <= d.y + d.h)
                or (d.x + d.w <= self.judge.x <= d.x + d.w + self.judge.r and d.y <= self.judge.y <= d.y + d.h)
                or (d.x <= self.judge.x <= d.x + d.w and d.y + d.h <= self.judge.y <= d.y + d.h + self.judge.r)
            ):
                d.alive = False
                self.player.hp -= 1
                
                if self.player.hp <= 0:
                    self.player.alive = False
                    self.scene = SCENE_GAMEOVER
                else:
                    self.player.urv = True

        if self.player.urv == True:
            self.player.damage_count += 1

        if self.player.damage_count > 400:
            self.player.damage_count = 0
            self.player.urv = False

        update_list(bullet_list)
        update_list(e_bullet_list)
        update_list(e_knife_list)
        update_list(enemy_list)
        update_list(blast_list)

        cleanup_list(bullet_list)
        cleanup_list(e_bullet_list)
        cleanup_list(e_knife_list)
        cleanup_list(enemy_list)
        cleanup_list(blast_list)

    def update_gameover_scene(self):
        update_list(bullet_list)
        update_list(e_bullet_list)
        update_list(e_knife_list)
        update_list(enemy_list)
        update_list(blast_list)

        cleanup_list(bullet_list)
        cleanup_list(e_bullet_list)
        cleanup_list(e_knife_list)
        cleanup_list(enemy_list)
        cleanup_list(blast_list)

    def draw(self):
        pyxel.cls(1)

        self.background.draw()

        if self.scene == SCENE_TITLE:
            self.draw_title_scene()

        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()

        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()

        pyxel.text(3,3, "SCORE {:5}".format(self.score), 7)

    def draw_title_scene(self):
        pyxel.text(73, 60, "Holo Shooter", 11)
        pyxel.text(66, 190, "- PRESS ENTER -", 13)

    def draw_play_scene(self):
        self.player.draw()
        self.judge.draw(self.player.x + PLAYER_WIDTH/2, self.player.y + PLAYER_HEIGHT/2)

        draw_list(bullet_list)
        draw_list(e_bullet_list)
        draw_list(e_knife_list)
        draw_list(enemy_list)
        draw_list(blast_list)

        pyxel.text(2, pyxel.height-7, "HP:{}".format(self.player.hp), 14)
        pyxel.text(pyxel.width-50, pyxel.height-7, "MUTEKI:{}".format(self.player.urv), 7)

    def draw_gameover_scene(self):
        draw_list(bullet_list)
        draw_list(e_bullet_list)
        draw_list(e_knife_list)
        draw_list(enemy_list)
        draw_list(blast_list)

        pyxel.text(75, 66, "GAME OVER", 8)
        
        
App()