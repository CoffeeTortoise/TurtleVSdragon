import pygame as pg
import sys
sys.path.append('engine')
from sprites import MonoSprite
from config import WND_HEIGHT, SIZE


SPEED: int = int(SIZE * .3)


def reflect(value: int, positive: bool = True) -> int:
    if value > 0 and not positive:
        value *= -1
    if value < 0 and positive:
        value *= -1
    return value


class Turtle(MonoSprite):
    def __init__(self,
                 image: pg.Surface,
                 pos: tuple[int, int],
                 sizes: tuple[int, int],
                 speed: int = SPEED,
                 alive: bool = True,
                 flip_x: bool = False,
                 shiftable: bool = True) -> None:
        super().__init__(image, pos, sizes, flip_x, shiftable)
        self.bounds_y: tuple[int, int] = 0, WND_HEIGHT - self.rect.height
        self.speed: int = speed
        self.alive: bool = alive

    def draw(self, wnd: pg.Surface) -> None:
        if self.alive:
            wnd.blit(self.image, self.rect)

    def update(self) -> None:
        if self.alive:
            self.key_move()

    def key_move(self) -> None:
        keys: pg.key.ScancodeWrapper = pg.key.get_pressed()
        if keys[pg.K_UP]:
            speed: int = reflect(self.speed, positive=False)
            self.rect.move_ip(0, speed)
        if keys[pg.K_DOWN]:
            speed: int = reflect(self.speed)
            self.rect.move_ip(0, speed)
        self.check_height()

    def check_height(self) -> None:
        y: int = self.rect.top
        if y < self.bounds_y[0]:
            speed: int = reflect(self.speed)
            self.rect.move_ip(0, speed)
        if y > self.bounds_y[1]:
            speed: int = reflect(self.speed, positive=False)
            self.rect.move_ip(0, speed)
    
