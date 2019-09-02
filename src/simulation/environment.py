import numpy as np

class Environment:
    """Represent the simulation landscape (the Nile River)."""

    def __init__(self, river_map, fertility_map, shape, const_config):
        """Initialise environment attributes upon object instantiation.

        Keyword arguments:
        river_map           -- numpy array with river pixels having a value of 1.0
        fertility_map       -- numpy array with fertility pixels between 0.0 and 1.0
                               (river and arrid land have a pixel value of 0.0 )
        shape               -- shape of all map attributes (tuple)
        """
        self.FLOOD_FREQ = const_config['flood_frequency']
        self.river_map = river_map
        self.fertility_map = fertility_map
        self.flood_map = np.copy(fertility_map)
        self.shape = shape

    def flood(self, generation):
        if self.FLOOD_FREQ and generation % self.FLOOD_FREQ == 0:
            self.fertility_map = self.flood_map
            self.flood_map = np.copy(self.fertility_map)
