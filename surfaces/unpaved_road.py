from surfaces.surface import Surface


class Sand(Surface):
    def __init__(self, position, image_path):
        super().__init__(
            position=position, image_path=image_path, type="road", slowing_power=1
        )
