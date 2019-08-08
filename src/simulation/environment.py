import numpy as np

class Environment:
    def __init__(self, river_map, fertility_map, shape):
        self.river_map = river_map
        self.fertility_map = fertility_map
        self.flood_map = np.copy(fertility_map)
        self.territory_map = np.zeros(shape) # TODO: currently unused
        self.claim_map = np.zeros(shape)
        self.shape = shape
