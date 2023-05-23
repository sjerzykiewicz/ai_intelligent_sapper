import pygame


class ScreenDrawer:
    BLACK = (0, 0, 0)
    WHITE = (200, 200, 200)

    def __init__(
        self,
        sapper,
        screen,
        clock,
        surfaces,
        landmine_surf,
        flag_surf,
        BLOCK_SIZE,
        WINDOW_WIDTH,
        WINDOW_HEIGHT,
        is_landmine_here,
        occupied_blocks,
        fence,
        barrels,
    ):
        self.sapper = sapper
        self.screen = screen
        self.clock = clock
        self.surfaces = surfaces
        self.landmine_surf = landmine_surf
        self.flag_surf = flag_surf
        self.BLOCK_SIZE = BLOCK_SIZE
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.is_landmine_here = is_landmine_here
        self.occupied_blocks = occupied_blocks
        self.fence = fence
        self.barrels = barrels

    def draw_screen(self) -> None:
        self._draw_screen()

    def _draw_screen(self) -> None:
        self.screen.fill(self.BLACK)
        self._draw_grid()
        self._draw_landmines()
        self._draw_fence()
        self._draw_goal()
        self._draw_sapper()
        self._draw_barrels()

        pygame.display.update()

    def _draw_sapper(self) -> None:
        self.screen.blit(self.sapper.get_surf(), self.sapper.get_rect())

    def _draw_landmines(self) -> None:
        for row in range(len(self.is_landmine_here)):
            for col in range(len(self.is_landmine_here[0])):
                if self.is_landmine_here[row][col]:
                    x, y = row * self.BLOCK_SIZE, col * self.BLOCK_SIZE
                    bomb_rect = self.landmine_surf.get_rect(topleft=(x, y))
                    self.screen.blit(self.landmine_surf, bomb_rect)

    def _draw_grid(self) -> None:
        for surface, rect in self.surfaces:
            self.screen.blit(surface, rect)

    def _draw_fence(self) -> None:
        for fence, rect in self.fence:
            self.screen.blit(fence, rect)

    def _draw_barrels(self) -> None:
        for barrel, rect in self.barrels:
            self.screen.blit(barrel, rect)

    def _draw_goal(self) -> None:
        goal = self.sapper.get_goal()
        x, y = goal[0] * self.BLOCK_SIZE, goal[1] * self.BLOCK_SIZE
        if (goal[0], goal[1]) not in self.occupied_blocks:
            flag_rect = self.flag_surf.get_rect(topleft=(x, y))
            self.screen.blit(self.flag_surf, flag_rect)
