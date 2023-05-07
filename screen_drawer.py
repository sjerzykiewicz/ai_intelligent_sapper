import pygame


class ScreenDrawer:
    BLACK = (0, 0, 0)
    WHITE = (200, 200, 200)

    def __init__(self, sapper, screen, clock, grass_surf, rects, landmine_surf, flag_surf, BLOCK_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, is_landmine_here, occupied_blocks):
        
        self.sapper = sapper
        self.screen = screen
        self.clock = clock
        self.grass_surf = grass_surf
        self.rects = rects
        self.landmine_surf = landmine_surf
        self.flag_surf = flag_surf
        self.BLOCK_SIZE = BLOCK_SIZE
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.is_landmine_here = is_landmine_here
        self.occupied_blocks = occupied_blocks

        self.fence_vertical = pygame.image.load("gfx/fence/fence_1.png").convert_alpha()
        self.fence_horizontal = pygame.image.load("gfx/fence/fence_2.png").convert_alpha()
        self.fence_corner_1 = pygame.image.load("gfx/fence/fence_3.png").convert_alpha()
        self.fence_corner_2 = pygame.image.load("gfx/fence/fence_4.png").convert_alpha()
        self.fence_corner_3 = pygame.image.load("gfx/fence/fence_5.png").convert_alpha()
        self.fence_corner_4 = pygame.image.load("gfx/fence/fence_6.png").convert_alpha()

    def draw(self):
        self._draw_screen()

    def _draw_screen(self):
        self.screen.fill(self.BLACK)
        self._draw_grid()
        self._draw_landmines()
        self._draw_fence()
        self._draw_goal()
        self._draw_sapper()

        pygame.display.update()

    def _draw_sapper(self):
        self.screen.blit(self.sapper.get_surf(), self.sapper.get_rect())

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

        for y in range(
            self.BLOCK_SIZE, self.WINDOW_HEIGHT - self.BLOCK_SIZE, self.BLOCK_SIZE
        ):
            self.screen.blit(self.fence_vertical, (0, y))
            self.screen.blit(self.fence_vertical, (self.WINDOW_WIDTH - self.BLOCK_SIZE, y))

        for x in range(
            self.BLOCK_SIZE, self.WINDOW_WIDTH - self.BLOCK_SIZE, self.BLOCK_SIZE
        ):
            self.screen.blit(self.fence_horizontal, (x, 0))
            self.screen.blit(
                self.fence_horizontal, (x, self.WINDOW_HEIGHT - self.BLOCK_SIZE)
            )

        self.screen.blit(self.fence_corner_1, (0, 0))
        self.screen.blit(self.fence_corner_2, (self.WINDOW_WIDTH - self.BLOCK_SIZE, 0))
        self.screen.blit(self.fence_corner_3, (0, self.WINDOW_HEIGHT - self.BLOCK_SIZE))
        self.screen.blit(
            self.fence_corner_4,
            (self.WINDOW_WIDTH - self.BLOCK_SIZE, self.WINDOW_HEIGHT - self.BLOCK_SIZE),
        )

    def _draw_goal(self):
        goal = self.sapper.get_goal()
        x, y = goal[0] * self.BLOCK_SIZE, goal[1] * self.BLOCK_SIZE
        if (goal[0], goal[1]) not in self.occupied_blocks:
            flag_rect = self.flag_surf.get_rect(topleft=(x, y))
            self.screen.blit(self.flag_surf, flag_rect)
