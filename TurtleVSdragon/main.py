import pygame as pg
from engine.tilemap import PhonePicture
from engine.config import WND_SIZE, SIZE, FPS
from engine.text import Counter, FNT_SIZE
from engine.enumerations import MousePressed
from engine.gui import Button
from engine.tools import SaveLoad, Timer
from engine.bullet import BulletSprite
from engine.colors import BLACK
from engine.player import Turtle
from engine.monster import Dragon
from paths import*


TITLE: str = 'Turtle vs Dragon'
ICON: str = TURTLE


pg.init()
pg.display.set_caption(TITLE)
WND: pg.Surface = pg.display.set_mode(WND_SIZE, pg.HWSURFACE)
icon: pg.Surface = pg.image.load(ICON).convert_alpha()
pg.display.set_icon(icon)


class Game:
    def __init__(self) -> None:

        # Common game objects
        self.clock: pg.time.Clock = pg.time.Clock()
        self.running: bool = True
        phone_pos: tuple[int, int] = 0, 0
        self.phone: PhonePicture = PhonePicture(phone_pos)
        self.loaded: bool = False
        self.saved: bool = False
        max_score: str = SaveLoad.load(FILE)
        self.max_score: int = int(max_score)

        # Game loop objects
        turtle_sizes: tuple[int, int] = SIZE * 6, SIZE * 3
        self.turtle_pos: tuple[int, int] = SIZE * 2, turtle_sizes[1] + SIZE
        turtle_img: pg.Surface = pg.image.load(TURTLE).convert_alpha()
        self.turtle: Turtle = Turtle(turtle_img, self.turtle_pos, turtle_sizes)
        dragon_sizes: tuple[int, int] = SIZE * 4, SIZE * 5
        self.dragon_pos: tuple[int, int] = WND_SIZE[0] - SIZE * 5, dragon_sizes[1] + SIZE
        dragon_img: pg.Surface = pg.image.load(DRAGON).convert_alpha()
        bullet_img: pg.Surface = pg.image.load(FIREBALL).convert_alpha()
        self.dragon: Dragon = Dragon(FIRE_MUS, dragon_img, bullet_img, self.dragon_pos, dragon_sizes, flip_x=True)
        self.bullet_list: list[BulletSprite] = []
        self.timer: Timer = Timer()
        self.score_counter: Counter = Counter(FONT)
        self.score: Counter = Counter(FONT, text='MAX SCORE:', start_value=self.max_score)
        max_score_pos: tuple[int, int] = WND_SIZE[0] - self.score.sizes[0] - SIZE * 2, 0
        self.score.pos = max_score_pos

        # Death loop objects
        fnt_size2: int = FNT_SIZE * 2
        txt1: str = 'RESTART'
        pos1: tuple[int, int] = int(WND_SIZE[0] * .5) - SIZE * 7, SIZE * 10
        self.button_restart: Button = Button(txt1, FONT, pos1, fnt_size2)
        txt2: str = 'QUIT'
        pos2: tuple[int, int] = pos1[0] + SIZE * 3, pos1[1] + SIZE * 5
        self.button_quit: Button = Button(txt2, FONT, pos2, fnt_size2)

        # Start game objects
        self.started: bool = False
        txt3: str = 'START'
        pos3: tuple[int, int] = pos1[0] + SIZE * 2, SIZE * 15
        self.button_start: Button = Button(txt3, FONT, pos3, fnt_size2)

        # Debug
        self.fps_list: list[float] = []

    def main(self) -> None:
        while self.running:
            WND.fill(BLACK)
            if self.turtle.alive:
                self.game_loop()
            else:
                self.over_loop()
            pg.display.flip()
            self.event_loop()
            self.clock.tick(FPS)
            self.fps_list.append(self.clock.get_fps())

    def game_loop(self) -> None:
        self.reload_score()
        self.phone.draw(WND)
        self.turtle.draw(WND)
        self.dragon.draw(WND)
        self.score.draw(WND)
        self.score_counter.draw(WND)
        if self.started:
            self.turtle.update()
            self.dragon.update()
            self.dragon.shoot(self.bullet_list)
            self.bullets()
            self.count_score()
        else:
            self.wait_loop()

    def wait_loop(self) -> None:
        self.button_start.draw(WND)
        self.button_start.update()
        if self.button_start.mouse == MousePressed.LEFT:
            self.started = True

    def over_loop(self) -> None:
        self.save_score()
        self.button_restart.draw(WND)
        self.button_quit.draw(WND)
        self.button_restart.update()
        self.button_quit.update()
        if self.button_restart.mouse == MousePressed.LEFT:
            self.restart()
        if self.button_quit.mouse == MousePressed.LEFT:
            self.running = False

    def restart(self) -> None:
        self.turtle.pos = self.turtle_pos
        self.dragon.pos = self.dragon_pos
        self.bullet_list.clear()
        self.timer.refresh()
        self.turtle.alive = True

    def reload_score(self) -> None:
        if not self.loaded:
            max_score: str = SaveLoad.load(FILE)
            self.max_score: int = int(max_score)
            self.score.change_value(self.max_score)
            self.loaded = True
            self.saved = False

    def save_score(self) -> None:
        if not self.saved:
            score: int = int(self.timer.get_time())
            if score > self.max_score:
                SaveLoad.save(FILE, score)
            self.saved = True
            self.loaded = False

    def count_score(self) -> None:
        score: int = int(self.timer.get_time())
        self.score_counter.change_value(score)

    def bullets(self) -> None:
        if len(self.bullet_list) == 0:
            return
        for bullet in self.bullet_list:
            if not bullet.exists:
                continue
            bullet.draw(WND)
            bullet.update()
            if bullet.bullet.rect.colliderect(self.turtle.rect):
                bullet.exists = False
                self.turtle.alive = False

    def event_loop(self) -> None:
        if not self.running:
            pg.quit()
            return
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                pg.quit()
                break
            else:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                        avg_fps: float = sum(self.fps_list) / len(self.fps_list)
                        print(f'{avg_fps=}')
                        pg.quit()
                        break


if __name__ == '__main__':
    game: Game = Game()
    game.main()
