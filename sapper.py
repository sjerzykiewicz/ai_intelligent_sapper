import pygame
from collections import deque
from queue import PriorityQueue

from bfs_state import BFSState
from a_star_state import AStarState


class Sapper:
    def __init__(self, pos, img, block_size, win_size, occupied_blocks, surfaces_types):
        self.speed = 10
        self.bombs_that_can_defuse = []
        self.capacity = 7
        self.occupied_blocks = occupied_blocks
        self.surfaces_types = surfaces_types

        self.surf = pygame.image.load(img).convert_alpha()
        self.rect = self.surf.get_rect(topleft=pos)
        self.origin_surf = self.surf
        self.block_size = block_size
        self.win_x, self.win_y = win_size
        self.angle = 0
        self.goal = (1, 1, 0)

        self.slowing_power = self._get_slowing_power()

    def get_surf(self) -> pygame.Surface:
        return self.surf

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def get_pos(self) -> tuple:
        return self.rect.x // self.block_size, self.rect.y // self.block_size

    def get_angle(self) -> int:
        return self.angle

    def get_goal(self) -> tuple:
        return self.goal

    def change_goal(self, new_goal) -> None:
        self.goal = new_goal

    def move_forward(self) -> None:
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

    def rotate(self, direction: str) -> None:
        if direction == "left":
            self.angle = (self.angle + 90) % 360
            self.surf = pygame.transform.rotate(self.origin_surf, self.angle)
        elif direction == "right":
            self.angle = (self.angle - 90) % 360
            self.surf = pygame.transform.rotate(self.origin_surf, self.angle)

    def auto_move_bfs(self, screen_drawer) -> None:
        path = self._find_path_bfs()
        self._auto_sapper_move(path, screen_drawer)

    def auto_move_a_star(self, screen_drawer) -> None:
        path = self._find_path_a_star()
        self._auto_sapper_move(path, screen_drawer)

    def _get_slowing_power(self) -> list:
        slowing_power = [
            [None for _ in range(len(self.surfaces_types[0]))]
            for _ in range(len(self.surfaces_types))
        ]
        for i in range(len(slowing_power)):
            for j in range(len(slowing_power[0])):
                if self.surfaces_types[i][j] == "unpaved_road":
                    slowing_power[i][j] = 1
                elif self.surfaces_types[i][j] == "grass":
                    slowing_power[i][j] = 5
                elif self.surfaces_types[i][j] == "sand":
                    slowing_power[i][j] = 25
        return slowing_power

    def _find_path_bfs(self) -> list:
        x = self.rect.x // self.block_size
        y = self.rect.y // self.block_size
        source = (x, y, self.angle)
        goal_state = self._search_state_space_bfs(source, self.goal)
        path = []
        while not goal_state.is_initial:
            path.append(goal_state.action)
            goal_state = goal_state.parent

        return path[::-1]

    def _search_state_space_bfs(self, initial_state, goal_state):
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
                    for next_state in self._get_succesor_states_bfs(cur_state):
                        queue.append((next_state))
        return BFSState(x_start, y_start, angle_state, None, None, True)

    def _get_succesor_states_bfs(self, state: BFSState) -> list:
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

    def _find_path_a_star(self) -> list:
        x = self.rect.x // self.block_size
        y = self.rect.y // self.block_size
        source = AStarState(
            x, y, self.angle, None, None, self.slowing_power[x][y], True
        )
        goal_x, goal_y, goal_angle = self.goal
        goal = AStarState(
            goal_x,
            goal_y,
            goal_angle,
            None,
            None,
            self.slowing_power[goal_x][goal_y],
        )
        goal_state = self._search_state_space_a_star(source, goal)
        path = []
        while not goal_state.is_initial:
            path.append(goal_state.action)
            goal_state = goal_state.parent

        return path[::-1]

    def _search_state_space_a_star(
        self, initial_state: AStarState, goal_state: AStarState
    ) -> AStarState:
        x_start, y_start, angle_state = initial_state.get_pos()
        x_end, y_end, _ = goal_state.get_pos()

        cnt = 0
        queue = PriorityQueue()
        queue.put((0, cnt, initial_state))
        visited_states = {(x_start, y_start, angle_state)}
        initial_state.g = 0
        initial_state.f = self._heuristic_a_star((x_start, y_start), (x_end, y_end))
        iteration_limit = 1_000_000

        while not queue.empty() and iteration_limit:
            cur_state = queue.get()[2]
            visited_states.remove(cur_state.get_pos())
            iteration_limit -= 1

            x, y, _ = cur_state.get_pos()
            if (x, y) == (x_end, y_end):
                return cur_state

            for next_state in self._get_succesor_states_a_star(cur_state):
                temp_g = cur_state.g + next_state.slowing_power

                if temp_g < next_state.g:
                    next_state.parent = cur_state
                    next_state.g = temp_g
                    next_x, next_y, _ = next_state.get_pos()
                    next_state.f = temp_g + self._heuristic_a_star(
                        (next_x, next_y), (x_end, y_end)
                    )
                    if next_state.get_pos() not in visited_states:
                        cnt += 1
                        queue.put((next_state.f, cnt, next_state))
                        visited_states.add(next_state.get_pos())

        return initial_state

    def _get_succesor_states_a_star(self, state: AStarState) -> list:
        x, y, angle = state.x, state.y, state.angle
        successors = []
        if angle == 0:
            if (x, y - 1) not in self.occupied_blocks:
                successors.append(
                    AStarState(x, y - 1, 0, state, "F", self.slowing_power[x][y - 1])
                )
        elif angle == 90:
            if (x - 1, y) not in self.occupied_blocks:
                successors.append(
                    AStarState(x - 1, y, 90, state, "F", self.slowing_power[x - 1][y])
                )
        elif angle == 180:
            if (x, y + 1) not in self.occupied_blocks:
                successors.append(
                    AStarState(x, y + 1, 180, state, "F", self.slowing_power[x][y + 1])
                )
        elif angle == 270:
            if (x + 1, y) not in self.occupied_blocks:
                successors.append(
                    AStarState(x + 1, y, 270, state, "F", self.slowing_power[x + 1][y])
                )

        successors.append(
            AStarState(x, y, (angle + 90) % 360, state, "L", self.slowing_power[x][y])
        )
        successors.append(
            AStarState(x, y, (angle - 90) % 360, state, "R", self.slowing_power[x][y])
        )
        return successors

    def _heuristic_a_star(self, p1: tuple, p2: tuple) -> int:
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    def time_bfs_and_a_star(self) -> None:
        bfs_path = self._find_path_bfs()
        a_star_path = self._find_path_a_star()

        print(self._get_time_to_move(bfs_path), self._get_time_to_move(a_star_path))

    def _auto_sapper_move(self, actions: list, screen_drawer) -> None:
        last_tick = pygame.time.get_ticks()

        for action in actions:
            if action == "L":
                self.rotate("left")
            elif action == "R":
                self.rotate("right")
            else:
                self.move_forward()

            screen_drawer.draw_screen()

            x, y = self.get_pos()

            ticks = 50

            if self.surfaces_types[x][y] == "sand":
                ticks = 200
            elif self.surfaces_types[x][y] == "grass":
                ticks = 100
            elif self.surfaces_types[x][y] == "unpaved_road":
                ticks = 50

            while True:
                if pygame.time.get_ticks() - last_tick >= ticks:
                    last_tick = pygame.time.get_ticks()
                    break

    def _get_time_to_move(self, actions: list) -> int:
        cur_x, cur_y = self.get_pos()
        cur_angle = self.get_angle()
        answer = 0

        for action in actions:
            if action == "F":
                if cur_angle == 0:
                    cur_y -= 1
                elif cur_angle == 90:
                    cur_x -= 1
                elif cur_angle == 180:
                    cur_y += 1
                elif cur_angle == 270:
                    cur_x += 1
            elif action == "L":
                cur_angle = (cur_angle + 90) % 360
            elif action == "R":
                cur_angle = (cur_angle - 90) % 360

            if self.surfaces_types[cur_x][cur_y] == "sand":
                answer += 200
            elif self.surfaces_types[cur_x][cur_y] == "grass":
                answer += 100
            elif self.surfaces_types[cur_x][cur_y] == "unpaved_road":
                answer += 50

        return answer
