from sappers.rain_defusing_sapper import RainDefusingSapper
from sappers.standard_sapper import StandardSapper


class SapperFactory:
    def __init__(self):
        self._sapper_types = {
            "standard": StandardSapper,
            "rain_defusing": RainDefusingSapper,
        }

    def create_sapper(self, sapper_type, *args):
        return self._sapper_types[sapper_type](*args)
