class AStarState:
    def __init__(self, x, y, angle, parent, action, slowing_power, is_initial=False):
        self.x = x
        self.y = y
        self.angle = angle
        self.parent = parent
        self.action = action
        self.slowing_power = slowing_power
        self.is_initial = is_initial
        self.g = float("inf")
        self.f = float("inf")

    def get_pos(self):
        return (self.x, self.y, self.angle)
