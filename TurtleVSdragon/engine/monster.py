import pygame as pg
import sys
sys.path.append('engine')
from config import SIZE, WND_HEIGHT
from sprites import MonoSprite
from bullet import BulletSprite
from tools import Timer


SPEED: int = int(SIZE * .3)
TIME_RECHARGE: float = .3
BULLET_SIZES: tuple[int, int] = SIZE, SIZE


def reflect(value: int, positive: bool = True) -> int:
    if value > 0 and not positive:
        value *= -1
    if value < 0 and positive:
        value *= -1
    return value


class Dragon(MonoSprite):
    def __init__(self,
                 shoot_snd: str,
                 image: pg.Surface,
                 bullet_img: pg.Surface,
                 pos: tuple[int, int],
                 sizes: tuple[int, int],
                 speed: int = SPEED,
                 time_recharge: float = TIME_RECHARGE,
                 down: bool = True,
                 alive: bool = True,
                 charged: bool = True,
                 flip_x: bool = False,
                 shiftable: bool = True,
                 bullet_sizes: tuple[int, int] = BULLET_SIZES) -> None:
        super().__init__(image, pos, sizes, flip_x, shiftable)
        self.speed: int = speed
        self.time_recharge: float = time_recharge
        self.charged: bool = charged
        self.alive: bool = alive
        self.down: bool = down
        self.bounds_y: tuple[int, int] = 0, WND_HEIGHT - self.rect.height
        self.bullet_sizes: tuple[int, int] = bullet_sizes
        self.timer: Timer = Timer()
        self.bullet_img: pg.Surface = bullet_img
        self.sound: pg.mixer.Sound = pg.mixer.Sound(shoot_snd)

    def draw(self, wnd: pg.Surface) -> None:
        if self.alive:
            wnd.blit(self.image, self.rect)

    def update(self) -> None:
        if not self.alive:
            return
        if self.down:
            self.move_down()
        else:
            self.move_up()

    def shoot(self, bullet_list: list[BulletSprite]) -> None:
        if not self.alive:
            return
        self.recharge()
        if not self.charged:
            return
        self.charged = False
        self.sound.play()
        bullet: BulletSprite = BulletSprite(self.bullet_img, self.bullet_sizes)
        bullet.pos = self.rect.center
        bullet_list.append(bullet)

    def recharge(self) -> None:
        if self.charged:
            return
        time: float = self.timer.get_time()
        if time >= self.time_recharge:
            self.charged = True
            self.timer.restart()

    def move_down(self) -> None:
        speed: int = reflect(self.speed)
        self.rect.move_ip(0, speed)
        y: int = self.rect.top
        if y > self.bounds_y[1]:
            self.down = False

    def move_up(self) -> None:
        speed: int = reflect(self.speed, positive=False)
        self.rect.move_ip(0, speed)
        y: int = self.rect.top
        if y < self.bounds_y[0]:
            self.down = True
    
