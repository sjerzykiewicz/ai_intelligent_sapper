import pygame
from collections import deque


class Sapper:
    def __init__(self, pos, img, block_size, win_size, occupied_blocks):
        self.speed = 10
        self.bombs_that_can_defuse = []
        self.capacity = 7
        self.occupied_blocks = occupied_blocks

        self.surf = pygame.image.load(img).convert_alpha()
        self.rect = self.surf.get_rect(topleft=pos)
        self.origin_surf = self.surf
        self.block_size = block_size
        self.win_x, self.win_y = win_size
        self.angle = 0

    def move_forward(self):
        if self.angle == 0:
            if (
                self.rect.x // self.block_size,
                self.rect.y // self.block_size - 1,
            ) not in self.occupied_blocks:
                self.rect.top -= self.block_size
        if self.angle == 90:
            if (
                self.rect.x // self.block_size - 1,
                self.rect.y // self.block_size,
            ) not in self.occupied_blocks:
                self.rect.left -= self.block_size
        if self.angle == 180:
            if (
                self.rect.x // self.block_size,
                self.rect.y // self.block_size + 1,
            ) not in self.occupied_blocks:
                self.rect.top += self.block_size
        if self.angle == 270:
            if (
                self.rect.x // self.block_size + 1,
                self.rect.y // self.block_size,
            ) not in self.occupied_blocks:
                self.rect.left += self.block_size

    def rotate(self, direction):
        if direction == "left":
            self.angle = (self.angle + 90) % 360
            self.surf = pygame.transform.rotate(self.origin_surf, self.angle)
        elif direction == "right":
            self.angle = (self.angle - 90) % 360
            self.surf = pygame.transform.rotate(self.origin_surf, self.angle)

    def move_up(self):
        x = self.rect.x // self.block_size
        y = self.rect.y // self.block_size
        path = self._find_path((x, y, self.angle), (1, 1))
        return path

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
    
    def _find_path(self, initial_state, goal_state):
        queue = deque()
        visited_states = set()
        queue.append((initial_state, []))
        while queue:
            cur_state, path = queue.popleft()
            x, y, angle = cur_state
            if (x, y, angle) not in visited_states:
                visited_states.add((x, y, angle))
                if (x, y) == goal_state:
                    return path
                else:
                    for neighbor in self._get_neighbor_states(cur_state):
                        queue.append((neighbor, path + [neighbor]))
        return None
    
    def _get_neighbor_states(self, state):
        # the neighbor states can be either going forward (make sure they're not in the self.occupied_blocks) or making a turn left or right
        # the state is a tuple of (x, y, angle)
        x, y, angle = state
        neighbors = []
        # the robot can only go forward
        if angle == 0:
            if (x, y - 1) not in self.occupied_blocks:
                neighbors.append((x, y - 1, 0))
        elif angle == 90:
            if (x - 1, y) not in self.occupied_blocks:
                neighbors.append((x - 1, y, 90))
        elif angle == 180:
            if (x, y + 1) not in self.occupied_blocks:
                neighbors.append((x, y + 1, 180))
        elif angle == 270:
            if (x + 1, y) not in self.occupied_blocks:
                neighbors.append((x + 1, y, 270))
        
        # the robot can turn left or right
        neighbors.append((x, y, (angle + 90) % 360))
        neighbors.append((x, y, (angle - 90) % 360))
        return neighbors
