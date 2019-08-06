import numpy as np

class Environment:
    def __init__(self, map, shape):
        self.map = map
        self.fertility_map = np.copy(map)
        self.territory_map = np.zeros(shape) # will add functionality related to this at some later point.
        self.claim_map = np.zeros(shape)
        self.shape = shape

    def flood(self):
        self.fertility_map = np.copy(self.map)
