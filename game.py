import pygame
from sapper import Sapper
import sys
from screen_drawer import ScreenDrawer
from threading import Thread


class Game:
    BLACK = (0, 0, 0)
    WHITE = (200, 200, 200)
    WINDOW_WIDTH = 1184
    WINDOW_HEIGHT = 736
    BLOCK_SIZE = 32

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Intelligent Sapper")
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        grass_path = "gfx/surfaces/grass.png"
        self.grass_surf = pygame.image.load(grass_path).convert_alpha()
        self.rects = self._create_grid_rects()

        landmine_path = "gfx/bombs/landmine.png"
        self.landmine_surf = pygame.image.load(landmine_path).convert_alpha()
        rows, columns = (
            self.WINDOW_WIDTH // self.BLOCK_SIZE,
            self.WINDOW_HEIGHT // self.BLOCK_SIZE,
        )
        self.is_landmine_here = [[False for _ in range(columns)] for _ in range(rows)]
        self.occupied_blocks = set()
        self._get_occupied_blocks()

        sapper_path = "gfx/sapper/sapper.png"
        self.sapper = Sapper(
            (576, 672),
            sapper_path,
            self.BLOCK_SIZE,
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT),
            self.occupied_blocks,
        )

        self.flag_path = "gfx/flags/flag.png"
        self.flag_surf = pygame.image.load(self.flag_path).convert_alpha()

        self.screen_drawer = ScreenDrawer(self.sapper, self.screen, self.clock, self.grass_surf, self.rects, self.landmine_surf, self.flag_surf, self.BLOCK_SIZE, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.is_landmine_here, self.occupied_blocks)


    def run(self):
        while True:
            self._handle_events()
            self.screen_drawer.draw()
            self._game_logic()
            self.clock.tick(60)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.sapper.move_forward()
                if event.key == pygame.K_LEFT:
                    self.sapper.rotate("left")
                if event.key == pygame.K_RIGHT:
                    self.sapper.rotate("right")
                if event.key == pygame.K_g:
                    self.sapper.auto_move(self.screen_drawer)
                if event.key == pygame.K_s:
                    x, y = pygame.mouse.get_pos()
                    x //= self.BLOCK_SIZE
                    y //= self.BLOCK_SIZE
                    self.sapper.change_goal((x, y, 0))

            mouse_pressed = pygame.mouse.get_pressed()
            x, y = pygame.mouse.get_pos()
            x //= self.BLOCK_SIZE
            y //= self.BLOCK_SIZE
            if mouse_pressed[0]:
                self.is_landmine_here[x][y] = True
                self.occupied_blocks.add((x, y))

            if mouse_pressed[2]:
                if self.is_landmine_here[x][y]:
                    self.occupied_blocks.remove((x, y))
                self.is_landmine_here[x][y] = False

    def _game_logic(self):
        pass

    def _create_grid_rects(self):
        rects = []
        for x in range(0, self.WINDOW_WIDTH, self.BLOCK_SIZE):
            for y in range(0, self.WINDOW_HEIGHT, self.BLOCK_SIZE):
                rect = self.grass_surf.get_rect(topleft=(x, y))
                rects.append(rect)
        return rects


    def _get_occupied_blocks(self):

        for y in range(
            self.BLOCK_SIZE, self.WINDOW_HEIGHT - self.BLOCK_SIZE, self.BLOCK_SIZE
        ):
            self.occupied_blocks.add((0, y // self.BLOCK_SIZE))
            self.occupied_blocks.add(
                (
                    (self.WINDOW_WIDTH - self.BLOCK_SIZE) // self.BLOCK_SIZE,
                    y // self.BLOCK_SIZE,
                )
            )

        for x in range(
            self.BLOCK_SIZE, self.WINDOW_WIDTH - self.BLOCK_SIZE, self.BLOCK_SIZE
        ):

            self.occupied_blocks.add((x // self.BLOCK_SIZE, 0))
            self.occupied_blocks.add(
                (
                    x // self.BLOCK_SIZE,
                    (self.WINDOW_HEIGHT - self.BLOCK_SIZE) // self.BLOCK_SIZE,
                )
            )

        self.occupied_blocks.add((0, 0))
        self.occupied_blocks.add(
            ((self.WINDOW_WIDTH - self.BLOCK_SIZE) // self.BLOCK_SIZE, 0)
        )
        self.occupied_blocks.add(
            (0, (self.WINDOW_HEIGHT - self.BLOCK_SIZE) // self.BLOCK_SIZE)
        )
        self.occupied_blocks.add(
            (
                (self.WINDOW_WIDTH - self.BLOCK_SIZE) // self.BLOCK_SIZE,
                (self.WINDOW_HEIGHT - self.BLOCK_SIZE) // self.BLOCK_SIZE,
            )
        )
        