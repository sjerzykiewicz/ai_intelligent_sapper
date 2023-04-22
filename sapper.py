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

    def find_path(self):
        x = self.rect.x // self.block_size
        y = self.rect.y // self.block_size
        source = (x, y, self.angle)
        goal = (1, 1, 0)
        path = self._search_state_space(source, goal)
        return path

    def get_surf(self):
        return self.surf

    def get_rect(self):
        return self.rect

    def get_pos(self):
        return self.rect.x // self.block_size, self.rect.y // self.block_size
    
    def _search_state_space(self, initial_state, goal_state):
        queue = deque()
        visited_states = set()
        x_end, y_end, _ = goal_state
        queue.append((initial_state, []))
        while queue:
            cur_state, path = queue.popleft()
            x, y, angle = cur_state
            if (x, y, angle) not in visited_states:
                visited_states.add((x, y, angle))
                if (x, y) == (x_end, y_end):
                    return path
                else:
                    for neighbor in self._get_succesor_states(cur_state):
                        queue.append((neighbor, path + [neighbor]))
        return None
    
    def _get_succesor_states(self, state):
        x, y, angle = state
        successors = []
        if angle == 0:
            if (x, y - 1) not in self.occupied_blocks:
                successors.append((x, y - 1, 0))
        elif angle == 90:
            if (x - 1, y) not in self.occupied_blocks:
                successors.append((x - 1, y, 90))
        elif angle == 180:
            if (x, y + 1) not in self.occupied_blocks:
                successors.append((x, y + 1, 180))
        elif angle == 270:
            if (x + 1, y) not in self.occupied_blocks:
                successors.append((x + 1, y, 270))
        
        successors.append((x, y, (angle + 90) % 360))
        successors.append((x, y, (angle - 90) % 360))
        return successors
