from bomb import Bomb


class Landmine(Bomb):
    
    def __init__(self, position, image_path, time_to_defuse, purpose):
        super().__init__(position=position, image_path=image_path, defusable=True)

        self.time_to_defuse = time_to_defuse
        self.purpose = purpose
        