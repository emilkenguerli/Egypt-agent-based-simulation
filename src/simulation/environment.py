import numpy as np

class Environment:
    def __init__(self, river_map, flood_map, shape):
        self.river_map = river_map
        self.flood_map = flood_map
        self.fertility_map = np.copy(flood_map)
        self.territory_map = np.zeros(shape) # will add functionality related to this at some later point.
        self.claim_map = np.zeros(shape)
        self.shape = shape

    def flood(self):
        self.fertility_map = np.copy(self.flood_map)
