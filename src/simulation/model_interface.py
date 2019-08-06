from abc import ABC, abstractmethod
import random

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
        rows, columns = environment.shape
        x, y = random.randint(0, columns), random.randint(0, rows)
        # TODO: an implicit assumption is being made here.
        return (x, y)
