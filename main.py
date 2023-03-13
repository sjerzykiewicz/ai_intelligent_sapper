import sys
import pygame
from sapper import Sapper


# move these constants to separate files
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_WIDTH = 1184
WINDOW_HEIGHT = 736
BLOCK_SIZE = 32


def handle_events(sapper):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    sapper.move_up()
                if event.key == pygame.K_s:
                    sapper.move_down()
                if event.key == pygame.K_a:
                    sapper.move_left()
                if event.key == pygame.K_d:
                    sapper.move_right()


def create_grid_rects():
    rects = []
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            rects.append(rect)
    return rects


def draw_grid(screen, rects):
    for rect in rects:
        pygame.draw.rect(screen, WHITE, rect, 1)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Intelligent Sapper')
    clock = pygame.time.Clock()

    sapper = Sapper((576, 672), 'gfx/sapper/sapper.png', BLOCK_SIZE, (WINDOW_WIDTH, WINDOW_HEIGHT))
    grid_rects = create_grid_rects()

    while True:
        handle_events(sapper)

        screen.fill(BLACK)
        draw_grid(screen, grid_rects)
        screen.blit(sapper.get_surf(), sapper.get_rect())
        
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
