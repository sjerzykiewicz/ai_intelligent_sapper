from landmine import Landmine


class Claymore(Landmine):
    
    def __init__(self, position, image_path, time_to_defuse, purpose, direction):
        super().__init__(position, image_path, time_to_defuse, purpose)

        self.direction = direction
