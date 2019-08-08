from abc import ABC, abstractmethod
import random

# TODO: the model should have a memory of all previous decisions.

class AbstractModel(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def generate_competency(self, min_competency):
        return random.uniform(min_competency, 1.0)

    @abstractmethod
    def generate_ambition(self, min_ambition):
        return random.uniform(min_ambition, 1.0)

    @abstractmethod
    def generate_position(self, environment):
        nrows, ncols = environment.shape
        x, y = random.randint(0, ncols-1), random.randint(0, nrows-1)
        return (x, y)

    @abstractmethod
    def choose_fields(self, environment):
        pass

    @abstractmethod
    def relocate(self, environment):
        pass
