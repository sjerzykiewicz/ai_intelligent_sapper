import pygame


class Sapper:
    def __init__(self, pos, img, block_size, win_size):
        self.speed = 10
        self.bombs_that_can_defuse = []
        self.capacity = 7

        self.surf = pygame.image.load(img).convert_alpha()
        self.rect = self.surf.get_rect(topleft=pos)
        self.origin_surf = self.surf
        self.block_size = block_size
        self.win_x, self.win_y = win_size
        self.angle = 0

    def move_up(self):
        if self.rect.y == self.block_size:
            return

        self.rect.top -= self.block_size
        if self.angle != 0:
            self.surf = self.origin_surf
            self.angle = 0

    def move_down(self):
        if self.rect.y == self.win_y - 2 * self.block_size:
            return

        self.rect.top += self.block_size
        if self.angle != 180:
            self.surf = pygame.transform.rotate(self.origin_surf, 180)
            self.angle = 180

    def move_right(self):
        if self.rect.x == self.win_x - 2 * self.block_size:
            return

        self.rect.left += self.block_size
        if self.angle != 270:
            self.surf = pygame.transform.rotate(self.origin_surf, 270)
            self.angle = 270

    def move_left(self):
        if self.rect.x == self.block_size:
            return

        self.rect.left -= self.block_size
        if self.angle != 90:
            self.surf = pygame.transform.rotate(self.origin_surf, 90)
            self.angle = 90

    def get_surf(self):
        return self.surf

    def get_rect(self):
        return self.rect

    def get_pos(self):
        return self.rect.x // self.block_size, self.rect.y // self.block_size
