import pygame
from sapper import Sapper
import sys


class Game():

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

        self.rects = self._create_grid_rects()

        sapper_path = "gfx/sapper/sapper.png"
        self.sapper = Sapper((576, 672), sapper_path, self.BLOCK_SIZE, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        landmine_path = "gfx/bombs/landmine.png"
        self.landmine_surf = pygame.image.load(landmine_path).convert_alpha()
        rows, columns = self.WINDOW_WIDTH // self.BLOCK_SIZE, self.WINDOW_HEIGHT // self.BLOCK_SIZE
        self.is_landmine_here = [[False for col in range(columns)] for row in range(rows)]

    
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
                if event.key == pygame.K_w:
                    self.sapper.move_up()
                if event.key == pygame.K_s:
                    self.sapper.move_down()
                if event.key == pygame.K_a:
                    self.sapper.move_left()
                if event.key == pygame.K_d:
                    self.sapper.move_right()
            
            mouse_pressed = pygame.mouse.get_pressed()
            x, y = pygame.mouse.get_pos()
            x //= self.BLOCK_SIZE
            y //= self.BLOCK_SIZE
            if mouse_pressed[0]:
                self.is_landmine_here[x][y] = True

            if mouse_pressed[2]:
                self.is_landmine_here[x][y] = False

    
    def _game_logic(self):
        return


    def _draw_screen(self):
        self.screen.fill(self.BLACK)
        self._draw_grid()
        self._draw_fence()
        self._draw_landmines()
        self.screen.blit(self.sapper.get_surf(), self.sapper.get_rect())

        pygame.display.update()

    
    def _draw_landmines(self):
        for row in range(len(self.is_landmine_here)):
            for col in range(len(self.is_landmine_here[0])):
                if self.is_landmine_here[row][col]:
                    x, y = row * self.BLOCK_SIZE, col * self.BLOCK_SIZE
                    bomb_rect = self.landmine_surf.get_rect(topleft = (x, y))
                    self.screen.blit(self.landmine_surf, bomb_rect)


    def _create_grid_rects(self):
        rects = []
        for x in range(0, self.WINDOW_WIDTH, self.BLOCK_SIZE):
            for y in range(0, self.WINDOW_HEIGHT, self.BLOCK_SIZE):
                rect = pygame.Rect(x, y, self.BLOCK_SIZE, self.BLOCK_SIZE)
                rects.append(rect)
        return rects


    def _draw_grid(self):
        for rect in self.rects:
            pygame.draw.rect(self.screen, self.WHITE, rect, 1)
            

    def _draw_fence(self):
        fence_vertical = pygame.image.load("gfx/fence/fence_1.png")
        fence_horizontal = pygame.image.load("gfx/fence/fence_2.png")
        fence_corner_1 = pygame.image.load("gfx/fence/fence_3.png")
        fence_corner_2 = pygame.image.load("gfx/fence/fence_4.png")
        fence_corner_3 = pygame.image.load("gfx/fence/fence_5.png")
        fence_corner_4 = pygame.image.load("gfx/fence/fence_6.png")
        
        for y in range(self.BLOCK_SIZE, self.WINDOW_HEIGHT - self.BLOCK_SIZE, self.BLOCK_SIZE):
            self.screen.blit(fence_vertical, (0, y))
            self.screen.blit(fence_vertical, (self.WINDOW_WIDTH - self.BLOCK_SIZE, y))
            
        for x in range(self.BLOCK_SIZE, self.WINDOW_WIDTH - self.BLOCK_SIZE, self.BLOCK_SIZE):
            self.screen.blit(fence_horizontal, (x, 0))
            self.screen.blit(fence_horizontal, (x, self.WINDOW_HEIGHT - self.BLOCK_SIZE))
        
        self.screen.blit(fence_corner_1, (0, 0))
        self.screen.blit(fence_corner_2, (self.WINDOW_WIDTH - self.BLOCK_SIZE, 0))
        self.screen.blit(fence_corner_3, (0, self.WINDOW_HEIGHT - self.BLOCK_SIZE))
        self.screen.blit(fence_corner_4, (self.WINDOW_WIDTH - self.BLOCK_SIZE, self.WINDOW_HEIGHT - self.BLOCK_SIZE))
