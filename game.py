import pygame
from sapper import Sapper
import sys
from screen_drawer import ScreenDrawer


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
        self.fence_vertical = pygame.image.load("gfx/fence/fence_1.png").convert_alpha()
        self.fence_horizontal = pygame.image.load(
            "gfx/fence/fence_2.png"
        ).convert_alpha()
        self.fence_corner_1 = pygame.image.load("gfx/fence/fence_3.png").convert_alpha()
        self.fence_corner_2 = pygame.image.load("gfx/fence/fence_4.png").convert_alpha()
        self.fence_corner_3 = pygame.image.load("gfx/fence/fence_5.png").convert_alpha()
        self.fence_corner_4 = pygame.image.load("gfx/fence/fence_6.png").convert_alpha()
        self.fence = self._create_fence()

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

        self.screen_drawer = ScreenDrawer(
            self.sapper,
            self.screen,
            self.clock,
            self.grass_surf,
            self.rects,
            self.landmine_surf,
            self.flag_surf,
            self.BLOCK_SIZE,
            self.WINDOW_WIDTH,
            self.WINDOW_HEIGHT,
            self.is_landmine_here,
            self.occupied_blocks,
            self.fence,
        )

    def run(self):
        while True:
            self._handle_events()
            self.screen_drawer.draw_screen()
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
                    if (x, y) not in self.occupied_blocks:
                        self.sapper.change_goal((x, y, 0))

            mouse_pressed = pygame.mouse.get_pressed()
            x, y = pygame.mouse.get_pos()
            x //= self.BLOCK_SIZE
            y //= self.BLOCK_SIZE
            if mouse_pressed[0]:
                if (x, y) not in self.occupied_blocks and 0 <= x < self.WINDOW_WIDTH // self.BLOCK_SIZE and 0 <= y < self.WINDOW_HEIGHT // self.BLOCK_SIZE:
                    self.is_landmine_here[x][y] = True
                    self.occupied_blocks.add((x, y))

            if mouse_pressed[2]:
                if 0 <= x < self.WINDOW_WIDTH // self.BLOCK_SIZE and 0 <= y < self.WINDOW_HEIGHT // self.BLOCK_SIZE:
                    if self.is_landmine_here[x][y]:
                        self.occupied_blocks.remove((x, y))
                    self.is_landmine_here[x][y] = False

    def _game_logic(self):
        pass

    # this method is called only once during the initialization of the game
    def _create_grid_rects(self):
        rects = []
        for x in range(0, self.WINDOW_WIDTH, self.BLOCK_SIZE):
            for y in range(0, self.WINDOW_HEIGHT, self.BLOCK_SIZE):
                rect = self.grass_surf.get_rect(topleft=(x, y))
                rects.append(rect)
        return rects

    # this method is called only once during the initialization of the game
    def _create_fence(self):
        fence = []

        for y in range(
            self.BLOCK_SIZE, self.WINDOW_HEIGHT - self.BLOCK_SIZE, self.BLOCK_SIZE
        ):
            rect = self.fence_vertical.get_rect(topleft=(0, y))
            fence.append([self.fence_vertical, rect])
            rect = self.fence_vertical.get_rect(
                topleft=(self.WINDOW_WIDTH - self.BLOCK_SIZE, y)
            )
            fence.append([self.fence_vertical, rect])

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
            rect = self.fence_horizontal.get_rect(topleft=(x, 0))
            fence.append([self.fence_horizontal, rect])
            rect = self.fence_horizontal.get_rect(
                topleft=(x, self.WINDOW_HEIGHT - self.BLOCK_SIZE)
            )
            fence.append([self.fence_horizontal, rect])

            self.occupied_blocks.add((x // self.BLOCK_SIZE, 0))
            self.occupied_blocks.add(
                (
                    x // self.BLOCK_SIZE,
                    (self.WINDOW_HEIGHT - self.BLOCK_SIZE) // self.BLOCK_SIZE,
                )
            )

        rect = self.fence_corner_1.get_rect(topleft=(0, 0))
        fence.append([self.fence_corner_1, rect])
        rect = self.fence_corner_2.get_rect(
            topleft=(self.WINDOW_WIDTH - self.BLOCK_SIZE, 0)
        )
        fence.append([self.fence_corner_2, rect])
        rect = self.fence_corner_3.get_rect(
            topleft=(0, self.WINDOW_HEIGHT - self.BLOCK_SIZE)
        )
        fence.append([self.fence_corner_3, rect])

        rect = self.fence_corner_4.get_rect(
            topleft=(
                self.WINDOW_WIDTH - self.BLOCK_SIZE,
                self.WINDOW_HEIGHT - self.BLOCK_SIZE,
            )
        )
        fence.append([self.fence_corner_4, rect])

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

        return fence
