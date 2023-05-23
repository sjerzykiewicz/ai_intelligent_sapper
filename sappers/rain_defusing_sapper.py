from sappers.sapper import Sapper


class RainDefusingSapper(Sapper):
    def __init__(self, pos, img, block_size, win_size, occupied_blocks, surfaces_types):
        super().__init__(pos, img, block_size, win_size, occupied_blocks, surfaces_types)
        self.can_defuse_in_rain = True
