from bomb import Bomb


class HarveysCasinoBomb(Bomb):

    def __init__(self, position, image_path, time_till_explosion):
        super().__init__(position=position, image_path=image_path, defusable=False)

        self.time_till_explosion = time_till_explosion
