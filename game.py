import pygame
from sappers.standard_sapper import StandardSapper
import sys
from screen_drawer import ScreenDrawer
from random import choices, randint


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

        unpaved_road_path = "gfx/surfaces/unpaved_road.png"
        self.unpaved_road_surf = pygame.image.load(unpaved_road_path).convert_alpha()

        sand_path = "gfx/surfaces/sand.png"
        self.sand_surf = pygame.image.load(sand_path).convert_alpha()

        self.surfaces, self.surfaces_types = self._create_grid_surfaces()

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

        barrel_path = "gfx/barrels/barrel.png"
        self.barrel_surf = pygame.image.load(barrel_path).convert_alpha()
        self.barrels = self._create_barrels()

        landmine_path = "gfx/bombs/landmine.png"
        self.landmine_surf = pygame.image.load(landmine_path).convert_alpha()
        claymore_path = "gfx/bombs/claymore.png"
        self.claymore_surf = pygame.image.load(claymore_path).convert_alpha()
        hcb = "gfx/bombs/hcb.png"
        self.hcb_surf = pygame.image.load(hcb).convert_alpha()

        self.bombs, self.bomb_types = self._create_bombs()

        sapper_path = "gfx/sapper/sapper.png"
        self.sapper = StandardSapper(
            (576, 672),
            sapper_path,
            self.BLOCK_SIZE,
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT),
            self.occupied_blocks,
            self.surfaces_types,
            self.bomb_types,
        )

        self.flag_path = "gfx/flags/flag.png"
        self.flag_surf = pygame.image.load(self.flag_path).convert_alpha()

        self.screen_drawer = ScreenDrawer(
            self.sapper,
            self.screen,
            self.clock,
            self.surfaces,
            self.landmine_surf,
            self.flag_surf,
            self.BLOCK_SIZE,
            self.WINDOW_WIDTH,
            self.WINDOW_HEIGHT,
            self.bombs,
            self.occupied_blocks,
            self.fence,
            self.barrels,
        )

    def run(self) -> None:
        while True:
            self._handle_events()
            self.screen_drawer.draw_screen()
            self._game_logic()
            self.clock.tick(60)

    def _handle_events(self) -> None:
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
                if event.key == pygame.K_b:
                    self.sapper.auto_move_bfs(self.screen_drawer)
                if event.key == pygame.K_a:
                    self.sapper.auto_move_a_star(self.screen_drawer)
                if event.key == pygame.K_t:
                    self.sapper.time_bfs_and_a_star()
                if event.key == pygame.K_s:
                    x, y = pygame.mouse.get_pos()
                    x //= self.BLOCK_SIZE
                    y //= self.BLOCK_SIZE
                    if (x, y) not in self.occupied_blocks:
                        self.sapper.change_goal((x, y, 0))

            # mouse_pressed = pygame.mouse.get_pressed()
            # x, y = pygame.mouse.get_pos()
            # x //= self.BLOCK_SIZE
            # y //= self.BLOCK_SIZE

    def _game_logic(self) -> None:
        pass

    # this method is called only once during the initialization of the game
    def _create_grid_surfaces(
        self,
    ) -> tuple[list[list[pygame.Surface]], list[list[str]]]:
        surfaces = []
        surfaces_types = [
            [None for _ in range(self.WINDOW_HEIGHT // self.BLOCK_SIZE)]
            for _ in range(self.WINDOW_WIDTH // self.BLOCK_SIZE)
        ]
        types_of_surfaces = ["grass", "unpaved_road", "sand"]
        weights = [50, 30, 20]
        for x in range(0, self.WINDOW_WIDTH, self.BLOCK_SIZE):
            for y in range(0, self.WINDOW_HEIGHT, self.BLOCK_SIZE):
                choice = choices(types_of_surfaces, weights=weights, k=1)[0]
                if choice == "unpaved_road":
                    rect = self.unpaved_road_surf.get_rect(topleft=(x, y))
                    surfaces.append([self.unpaved_road_surf, rect])
                elif choice == "grass":
                    rect = self.grass_surf.get_rect(topleft=(x, y))
                    surfaces.append([self.grass_surf, rect])
                elif choice == "sand":
                    rect = self.sand_surf.get_rect(topleft=(x, y))
                    surfaces.append([self.sand_surf, rect])

                i, j = x // self.BLOCK_SIZE, y // self.BLOCK_SIZE
                surfaces_types[i][j] = choice

        return surfaces, surfaces_types
    
    # this method is called only once during the initialization of the game
    def _create_bombs(self) -> tuple[list[list[pygame.Surface]], list[list[str]]]:
        bombs = []
        bombs_types = [
            [None for _ in range(self.WINDOW_HEIGHT // self.BLOCK_SIZE)]
            for _ in range(self.WINDOW_WIDTH // self.BLOCK_SIZE)
        ]
        types_of_bombs = ["none", "claymore", "landmine", "hcb"]
        weights = [500, 50, 30, 20]
        for x in range(0, self.WINDOW_WIDTH, self.BLOCK_SIZE):
            for y in range(0, self.WINDOW_HEIGHT, self.BLOCK_SIZE):
                i, j = x // self.BLOCK_SIZE, y // self.BLOCK_SIZE
                if (i, j) in self.occupied_blocks:
                    continue

                choice = choices(types_of_bombs, weights=weights, k=1)[0]
                if choice == "none":
                    continue
                elif choice == "claymore":
                    rect = self.claymore_surf.get_rect(topleft=(x, y))
                    bombs.append([self.claymore_surf, rect])
                elif choice == "landmine":
                    rect = self.landmine_surf.get_rect(topleft=(x, y))
                    bombs.append([self.landmine_surf, rect])
                elif choice == "hcb":
                    rect = self.hcb_surf.get_rect(topleft=(x, y))
                    bombs.append([self.hcb_surf, rect])

                bombs_types[i][j] = choice

        return bombs, bombs_types

    # this method is called only once during the initialization of the game
    def _create_fence(self) -> list[list]:
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
    
    # this method is called only once during the initialization of the game
    def _create_barrels(self) -> list[list]:
        barrels = []
        for _ in range(20):
            x = randint(0, self.WINDOW_WIDTH // self.BLOCK_SIZE - 1)
            y = randint(0, self.WINDOW_HEIGHT // self.BLOCK_SIZE - 1)
            if (x, y) not in self.occupied_blocks:
                rect = self.barrel_surf.get_rect(topleft=(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE))
                barrels.append([self.barrel_surf, rect])
                self.occupied_blocks.add((x, y))
        return barrels
