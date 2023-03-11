import sys
import pygame
from sapper import Sapper


# move these constants to separate files
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_WIDTH = 1184
WINDOW_HEIGHT = 736
BLOCK_SIZE = 32


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Intelligent Sapper')
    clock = pygame.time.Clock()

    sapper = Sapper(576, 672, 'gfx/sapper/sapper.png')

    while True:

        screen.fill(BLACK)
        # drawing the rectangles
        for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
            for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
                rectangle = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, WHITE, rectangle, 1)

        # checking for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    sapper.move_up(BLOCK_SIZE)
                if event.key == pygame.K_s:
                    sapper.move_down(BLOCK_SIZE)
                if event.key == pygame.K_a:
                    sapper.move_left(BLOCK_SIZE)
                if event.key == pygame.K_d:
                    sapper.move_right(BLOCK_SIZE)

        screen.blit(sapper.get_surf(), sapper.get_rect())
        
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
