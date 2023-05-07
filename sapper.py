import pygame
from collections import deque
from bfs_state import BFSState


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
        self.goal = (1, 1, 0)

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

    def auto_move(self, screen_drawer):
        path = self._find_path()
        self._auto_sapper_move(path, screen_drawer)

    def _find_path(self):
        x = self.rect.x // self.block_size
        y = self.rect.y // self.block_size
        source = (x, y, self.angle)
        end_state = self._search_state_space(source, self.goal)
        path = []
        while not end_state.is_initial:
            path.append(end_state.action)
            end_state = end_state.parent

        return path[::-1]

    def get_surf(self):
        return self.surf

    def get_rect(self):
        return self.rect

    def get_pos(self):
        return self.rect.x // self.block_size, self.rect.y // self.block_size

    def get_angle(self):
        return self.angle

    def _search_state_space(self, initial_state, goal_state):
        queue = deque()
        visited_states = set()
        x_start, y_start, angle_state = initial_state
        x_end, y_end, _ = goal_state
        queue.append(BFSState(x_start, y_start, angle_state, None, None, True))
        while queue:
            cur_state = queue.popleft()
            x, y, angle = cur_state.x, cur_state.y, cur_state.angle
            if (x, y, angle) not in visited_states:
                visited_states.add((x, y, angle))
                if (x, y) == (x_end, y_end):
                    return cur_state
                else:
                    for next_state in self._get_succesor_states(cur_state):
                        queue.append((next_state))
        return BFSState(x_start, y_start, angle_state, None, None, True)

    def _get_succesor_states(self, state):
        x, y, angle = state.x, state.y, state.angle
        successors = []
        forward = "F"
        if angle == 0:
            if (x, y - 1) not in self.occupied_blocks:
                successors.append(BFSState(x, y - 1, 0, state, forward))
        elif angle == 90:
            if (x - 1, y) not in self.occupied_blocks:
                successors.append(BFSState(x - 1, y, 90, state, forward))
        elif angle == 180:
            if (x, y + 1) not in self.occupied_blocks:
                successors.append(BFSState(x, y + 1, 180, state, forward))
        elif angle == 270:
            if (x + 1, y) not in self.occupied_blocks:
                successors.append(BFSState(x + 1, y, 270, state, forward))

        successors.append(BFSState(x, y, (angle + 90) % 360, state, "L"))
        successors.append(BFSState(x, y, (angle - 90) % 360, state, "R"))
        return successors

    def get_goal(self):
        return self.goal

    def change_goal(self, new_goal):
        self.goal = new_goal

    def _auto_sapper_move(self, actions, screen_drawer):
        last_tick = pygame.time.get_ticks()

        for action in actions:
            if action == "L":
                self.rotate("left")
            elif action == "R":
                self.rotate("right")
            else:
                self.move_forward()

            screen_drawer.draw()

            while True:
                if pygame.time.get_ticks() - last_tick >= 50:
                    last_tick = pygame.time.get_ticks()
                    break
