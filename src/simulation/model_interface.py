from abc import ABC, abstractmethod
import random

# TODO: the model should have a memory of all previous decisions
# as well as current stats associated with household.

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
    def relocate(self, household, environment):
        statistics = household.statistics()
        nrow, ncol = environment.shape
        num_workers = statistics['num_workers']
        knowledge_ratio = statistics['knowledge_ratio']
        x_pos, y_pos = statistics['x_pos'], statistics['y_pos']
        knowledge_radius = num_workers*knowledge_ratio
        new_x = x_pos + int(random.uniform(-knowledge_radius, knowledge_radius))
        new_y = y_pos + int(random.uniform(-knowledge_radius, knowledge_radius))
        if new_x < 0 or new_x > ncol-1:
            return (x_pos, y_pos)
        elif new_y < 0 or new_y > nrow-1:
            return (x_pos, y_pos)
        else:
            return (new_x, new_y)
