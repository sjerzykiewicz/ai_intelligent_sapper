from sappers.sapper import Sapper


class StandardSapper(Sapper):
    def __init__(
        self, pos, block_size, win_size, occupied_blocks, surfaces_types, bombs, goal
    ):
        super().__init__(
            pos,
            "gfx/sapper/sapper.png",
            block_size,
            win_size,
            occupied_blocks,
            surfaces_types,
            bombs,
            goal,
        )
        self.can_defuse_in_rain = False
