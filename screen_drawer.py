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
        bombs,
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
        self.bombs = bombs
        self.occupied_blocks = occupied_blocks
        self.fence = fence
        self.barrels = barrels

    def draw_screen(self) -> None:
        self._draw_screen()

    def _draw_screen(self) -> None:
        self.screen.fill(self.BLACK)
        self._draw_grid()
        self._draw_bombs()
        self._draw_fence()
        self._draw_goal()
        self._draw_sapper()
        self._draw_barrels()

        pygame.display.update()

    def _draw_sapper(self) -> None:
        self.screen.blit(self.sapper.get_surf(), self.sapper.get_rect())

    def _draw_bombs(self) -> None:
        for bomb, rect in self.bombs:
            self.screen.blit(bomb, rect)

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
        i, j, _ = self.sapper.get_goal()
        x, y = i * self.BLOCK_SIZE, j * self.BLOCK_SIZE
        if (i, j) not in self.occupied_blocks:
            flag_rect = self.flag_surf.get_rect(topleft=(x, y))
            self.screen.blit(self.flag_surf, flag_rect)
