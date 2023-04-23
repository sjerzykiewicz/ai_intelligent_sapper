import pygame
from sapper import Sapper
import sys


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

        self.laser_vertical = pygame.image.load("gfx/laser/laser_1.png").convert_alpha()
        self.laser_horizontal = pygame.image.load(
            "gfx/laser/laser_2.png"
        ).convert_alpha()
        self.laser_corner_1 = pygame.image.load("gfx/laser/laser_3.png").convert_alpha()
        self.laser_corner_2 = pygame.image.load("gfx/laser/laser_4.png").convert_alpha()
        self.laser_corner_3 = pygame.image.load("gfx/laser/laser_5.png").convert_alpha()
        self.laser_corner_4 = pygame.image.load("gfx/laser/laser_6.png").convert_alpha()
        self.laser_vertical.set_alpha(128)
        self.laser_horizontal.set_alpha(128)
        self.laser_corner_1.set_alpha(128)
        self.laser_corner_2.set_alpha(128)
        self.laser_corner_3.set_alpha(128)
        self.laser_corner_4.set_alpha(128)
        self.to_visualize = []
        self.to_visualize_done = False

        landmine_path = "gfx/bombs/landmine.png"
        self.landmine_surf = pygame.image.load(landmine_path).convert_alpha()
        rows, columns = (
            self.WINDOW_WIDTH // self.BLOCK_SIZE,
            self.WINDOW_HEIGHT // self.BLOCK_SIZE,
        )
        self.is_landmine_here = [[False for _ in range(columns)] for _ in range(rows)]
        self.occupied_blocks = set()

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

    def run(self):
        while True:
            self._handle_events()
            self._game_logic()
            self._draw_screen()
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
                if event.key == pygame.K_w:
                    self.to_visualize = self.sapper.find_path()
                    self.to_visualize_done = False
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
        sapper_x, sapper_y = self.sapper.get_pos()
        if self.is_landmine_here[sapper_x][sapper_y]:
            self.occupied_blocks.remove((sapper_x, sapper_y))
        self.is_landmine_here[sapper_x][sapper_y] = False

    def _draw_screen(self):
        self.screen.fill(self.BLACK)
        self._draw_grid()
        self._draw_landmines()
        self._draw_fence()
        self._visualize_path()
        self._draw_goal()
        self.screen.blit(self.sapper.get_surf(), self.sapper.get_rect())

        pygame.display.update()

    def _draw_landmines(self):
        for row in range(len(self.is_landmine_here)):
            for col in range(len(self.is_landmine_here[0])):
                if self.is_landmine_here[row][col]:
                    x, y = row * self.BLOCK_SIZE, col * self.BLOCK_SIZE
                    bomb_rect = self.landmine_surf.get_rect(topleft=(x, y))
                    self.screen.blit(self.landmine_surf, bomb_rect)

    def _create_grid_rects(self):
        rects = []
        for x in range(0, self.WINDOW_WIDTH, self.BLOCK_SIZE):
            for y in range(0, self.WINDOW_HEIGHT, self.BLOCK_SIZE):
                rect = self.grass_surf.get_rect(topleft=(x, y))
                rects.append(rect)
        return rects

    def _draw_grid(self):
        for rect in self.rects:
            self.screen.blit(self.grass_surf, rect)

    def _draw_fence(self):
        fence_vertical = pygame.image.load("gfx/fence/fence_1.png").convert_alpha()
        fence_horizontal = pygame.image.load("gfx/fence/fence_2.png").convert_alpha()
        fence_corner_1 = pygame.image.load("gfx/fence/fence_3.png").convert_alpha()
        fence_corner_2 = pygame.image.load("gfx/fence/fence_4.png").convert_alpha()
        fence_corner_3 = pygame.image.load("gfx/fence/fence_5.png").convert_alpha()
        fence_corner_4 = pygame.image.load("gfx/fence/fence_6.png").convert_alpha()

        for y in range(
            self.BLOCK_SIZE, self.WINDOW_HEIGHT - self.BLOCK_SIZE, self.BLOCK_SIZE
        ):
            self.screen.blit(fence_vertical, (0, y))
            self.screen.blit(fence_vertical, (self.WINDOW_WIDTH - self.BLOCK_SIZE, y))

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
            self.screen.blit(fence_horizontal, (x, 0))
            self.screen.blit(
                fence_horizontal, (x, self.WINDOW_HEIGHT - self.BLOCK_SIZE)
            )

            self.occupied_blocks.add((x // self.BLOCK_SIZE, 0))
            self.occupied_blocks.add(
                (
                    x // self.BLOCK_SIZE,
                    (self.WINDOW_HEIGHT - self.BLOCK_SIZE) // self.BLOCK_SIZE,
                )
            )

        self.screen.blit(fence_corner_1, (0, 0))
        self.screen.blit(fence_corner_2, (self.WINDOW_WIDTH - self.BLOCK_SIZE, 0))
        self.screen.blit(fence_corner_3, (0, self.WINDOW_HEIGHT - self.BLOCK_SIZE))
        self.screen.blit(
            fence_corner_4,
            (self.WINDOW_WIDTH - self.BLOCK_SIZE, self.WINDOW_HEIGHT - self.BLOCK_SIZE),
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

    def _visualize_path(self):
        if not self.to_visualize:
            return
        if self.to_visualize_done:
            x, y, rot = (
                self.to_visualize[-1][0] * self.BLOCK_SIZE,
                self.to_visualize[-1][1] * self.BLOCK_SIZE,
                self.to_visualize[-1][2],
            )
            if rot == 0 or rot == 180:
                laser_rect = self.laser_vertical.get_rect(topleft=(x, y))
                laser_surf = self.laser_vertical
                self.screen.blit(laser_surf, laser_rect)
            else:
                laser_rect = self.laser_horizontal.get_rect(topleft=(x, y))
                laser_surf = self.laser_horizontal
                self.screen.blit(laser_surf, laser_rect)

            for i in range(1, len(self.to_visualize) - 1):
                x, y, rot = (
                    self.to_visualize[i][0] * self.BLOCK_SIZE,
                    self.to_visualize[i][1] * self.BLOCK_SIZE,
                    self.to_visualize[i][2],
                )
                last_x, last_y, last_rot = (
                    self.to_visualize[i - 1][0] * self.BLOCK_SIZE,
                    self.to_visualize[i - 1][1] * self.BLOCK_SIZE,
                    self.to_visualize[i - 1][2],
                )

                next_x, next_y, next_rot = (
                    self.to_visualize[i + 1][0] * self.BLOCK_SIZE,
                    self.to_visualize[i + 1][1] * self.BLOCK_SIZE,
                    self.to_visualize[i + 1][2],
                )

                laser_rect = self.laser_vertical.get_rect(topleft=(x, y))
                laser_surf = self.laser_vertical

                if last_x != x:
                    laser_rect = self.laser_horizontal.get_rect(topleft=(x, y))
                    laser_surf = self.laser_horizontal

                if rot != last_rot:
                    if (rot == 180 and last_rot == 90) or (
                        rot == 270 and last_rot == 0
                    ):
                        laser_rect = self.laser_corner_1.get_rect(topleft=(x, y))
                        laser_surf = self.laser_corner_1
                    if (rot == 90 and last_rot == 0) or (
                        rot == 180 and last_rot == 270
                    ):
                        laser_rect = self.laser_corner_2.get_rect(topleft=(x, y))
                        laser_surf = self.laser_corner_2
                    if (rot == 0 and last_rot == 90) or (
                        rot == 270 and last_rot == 180
                    ):
                        laser_rect = self.laser_corner_3.get_rect(topleft=(x, y))
                        laser_surf = self.laser_corner_3
                    if (rot == 0 and last_rot == 270) or (
                        rot == 90 and last_rot == 180
                    ):
                        laser_rect = self.laser_corner_4.get_rect(topleft=(x, y))
                        laser_surf = self.laser_corner_4
                if rot == next_rot:
                    self.screen.blit(laser_surf, laser_rect)
            return

        for i in range(1, len(self.to_visualize) - 1):
            x, y, rot = (
                self.to_visualize[i][0] * self.BLOCK_SIZE,
                self.to_visualize[i][1] * self.BLOCK_SIZE,
                self.to_visualize[i][2],
            )
            last_x, last_rot = (
                self.to_visualize[i - 1][0] * self.BLOCK_SIZE,
                self.to_visualize[i - 1][2],
            )

            next_rot = self.to_visualize[i + 1][2]

            laser_rect = self.laser_vertical.get_rect(topleft=(x, y))
            laser_surf = self.laser_vertical

            if last_x != x:
                laser_rect = self.laser_horizontal.get_rect(topleft=(x, y))
                laser_surf = self.laser_horizontal

            if rot != last_rot:
                if (rot == 180 and last_rot == 90) or (rot == 270 and last_rot == 0):
                    laser_rect = self.laser_corner_1.get_rect(topleft=(x, y))
                    laser_surf = self.laser_corner_1
                if (rot == 90 and last_rot == 0) or (rot == 180 and last_rot == 270):
                    laser_rect = self.laser_corner_2.get_rect(topleft=(x, y))
                    laser_surf = self.laser_corner_2
                if (rot == 0 and last_rot == 90) or (rot == 270 and last_rot == 180):
                    laser_rect = self.laser_corner_3.get_rect(topleft=(x, y))
                    laser_surf = self.laser_corner_3
                if (rot == 0 and last_rot == 270) or (rot == 90 and last_rot == 180):
                    laser_rect = self.laser_corner_4.get_rect(topleft=(x, y))
                    laser_surf = self.laser_corner_4
            if rot == next_rot:
                self.screen.blit(laser_surf, laser_rect)

            pygame.display.update(laser_rect)
            pygame.time.wait(50)
        self.to_visualize_done = True

    def _draw_goal(self):
        goal = self.sapper.get_goal()
        x, y = goal[0] * self.BLOCK_SIZE, goal[1] * self.BLOCK_SIZE
        if (goal[0], goal[1]) not in self.occupied_blocks:
            flag_rect = self.flag_surf.get_rect(topleft=(x, y))
            self.screen.blit(self.flag_surf, flag_rect)
