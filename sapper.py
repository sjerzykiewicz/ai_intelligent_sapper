import pygame

class Sapper():
    def __init__(self, x, y, img):
        self.surf = pygame.image.load(img).convert_alpha()
        self.rect = self.surf.get_rect(topleft = (x, y))
        self.origin_surf = self.surf
        self.angle = 0
    
    def move_up(self, block_size):
        self.rect.top -= block_size
        if self.angle != 0:
            self.surf = self.origin_surf
            self.angle = 0
    
    def move_down(self, block_size):
        self.rect.top += block_size
        if self.angle != 180:
            self.surf = pygame.transform.rotate(self.origin_surf, 180)
            self.angle = 180
    
    def move_right(self, block_size):
        self.rect.left += block_size
        if self.angle != 90:
            self.surf = pygame.transform.rotate(self.origin_surf, 90)
            self.angle = 90
    
    def move_left(self, block_size):
        self.rect.left-= block_size
        if self.angle != 270:
            self.surf = pygame.transform.rotate(self.origin_surf, 270)
            self.angle = 270
        
    def get_surf(self):
        return self.surf
    
    def get_rect(self):
        return self.rect
    
    