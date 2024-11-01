import pygame as pg
import sys
sys.path.append('engine')
from config import SIZE, WND_SIZE
from colors import GREEN, BLUE
from interfaces import PseudoSurface


BLOCK_SIZES: tuple[int, int] = SIZE, SIZE
TILE: tuple[str, ...] = (
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        'GGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGG',
        )


class PhonePicture(PseudoSurface):
    def __init__(self,
                 pos: tuple[int, int],
                 block_sizes: tuple[int, int] = BLOCK_SIZES) -> None:
        self.surface: pg.Surface = pg.surface.Surface(WND_SIZE)
        for i, row in enumerate(TILE):
            for j, col in enumerate(row):
                block_pos: tuple[int, int] = SIZE * j, SIZE * i
                if col == 'B':
                    color: tuple[int, int, int] = BLUE
                else:
                    color: tuple[int, int, int] = GREEN
                rect: pg.rect.Rect = pg.rect.Rect(block_pos[0], block_pos[1], block_sizes[0], block_sizes[1])
                pg.draw.rect(self.surface, color, rect)
        self.rect: pg.rect.Rect = self.surface.get_rect()
        self.rect.left, self.rect.top = pos

    def draw(self, wnd: pg.Surface) -> None:
        wnd.blit(self.surface, self.rect)

    @property
    def pos(self) -> tuple[int, int]:
        return self.rect.left, self.rect.top

    @pos.setter
    def pos(self, pos: tuple[int, int]) -> None:
        if pos != (self.rect.left, self.rect.top):
            self.rect.left, self.rect.top = pos

    @property
    def sizes(self) -> tuple[int, int]:
        return self.rect.width, self.rect.height

    @sizes.setter
    def sizes(self, sizes: tuple[int, int]) -> None:
        if sizes != (self.rect.width, self.rect.height):
            self.surface: pg.Surface = pg.transform.scale(self.surface, sizes)
            pos: tuple[int, int] = self.rect.left, self.rect.top
            self.rect: pg.rect.Rect = self.surface.get_rect()
            self.rect.left, self.rect.top = pos

