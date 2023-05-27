from sappers.sapper import Sapper


class RainDefusingSapper(Sapper):
    def __init__(
        self, pos, block_size, win_size, occupied_blocks, surfaces_types, bombs, goal, weather, time_of_day
    ):
        super().__init__(
            pos,
            "gfx/sapper/sapper_red.png",
            block_size,
            win_size,
            occupied_blocks,
            surfaces_types,
            bombs,
            goal,
            weather,
            time_of_day,
        )
        self.can_defuse_in_rain = True
