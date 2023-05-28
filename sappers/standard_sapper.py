from sappers.sapper import Sapper


class StandardSapper(Sapper):
    def __init__(
        self, pos, block_size, win_size, occupied_blocks, surfaces_types, goal, weather, time_of_day, bombs,
    ):
        super().__init__(
            pos,
            "gfx/sapper/sapper.png",
            block_size,
            win_size,
            occupied_blocks,
            surfaces_types,
            goal,
            weather,
            time_of_day,
            bombs,
        )
        self.can_defuse_in_rain = False
