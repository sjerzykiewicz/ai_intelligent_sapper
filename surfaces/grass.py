from surfaces.surface import Surface


class Grass(Surface):
    def __init__(self, position, image_path):
        super().__init__(
            position=position, image_path=image_path, type="meadown", slowing_power=3
        )
