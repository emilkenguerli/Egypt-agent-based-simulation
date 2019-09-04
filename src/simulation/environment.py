import numpy as np

class Environment:
    """Represents the simulation landscape (the Nile River).

    Attributes:
        FLOOD_FREQ: Frequency in which a flood replenishes the land.
        river_map: numpy.ndarray in which river pixels have a value of 1.0 and
            the remaining pixels have a value of 0.0.
        fertility_map: numpy.ndarray in which fertility values vary between 0.0
            and 1.0.
        self.flood_map: numpy.ndarray that stores the original fertility_map.
        self.shape: A tuple recording the number of rows and columns of all
            maps.
    """

    def __init__(self, river_map, fertility_map, shape, const_config):
        """Initialises environment attributes upon instantiation.

        Args:
            river_map: numpy.ndarray in which river pixels have a value of 1.0
                and the remaining pixels have a value of 0.0.
            fertility_map: numpy.ndarray in which fertility values vary between
                0.0 and 1.0.
            self.shape: A tuple recording the number of rows and columns of
                environment (all maps have the same shape).
            const_config: A dictionary containing the constant start parameters
                of the simulation.
        """
        self.FLOOD_FREQ = const_config['flood_frequency']
        self.river_map = river_map
        self.fertility_map = fertility_map
        self.flood_map = np.copy(fertility_map)
        self.shape = shape

    def flood(self, generation):
        """Resets the fertility_map to its original fertility values."""
        if self.FLOOD_FREQ and generation % self.FLOOD_FREQ == 0:
            self.fertility_map = self.flood_map
            self.flood_map = np.copy(self.fertility_map)
