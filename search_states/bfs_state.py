class BFSState:
    def __init__(self, x, y, angle, parent, action, is_initial=False):
        self.x = x
        self.y = y
        self.angle = angle
        self.parent = parent
        self.action = action
        self.is_initial = is_initial
