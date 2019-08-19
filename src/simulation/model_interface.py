from abc import ABC, abstractmethod
import random

# TODO: the model should have a memory of all previous decisions
# as well as current stats associated with household.

class AbstractModel(ABC):
    """Interface describes household decision-making.

    Keyword arguments:
    ABC -- the abstract base class

    Each model instance serves as the decision-making core of a particular
    household. It contains the memory of previous generations and past decisions.
    Each method represents a possible decision, thus giving the household its
    autonomy.

    Implementation of abstract methods is unsophistacated. A derived class
    can either override or extend the functionality provided by this class.
    """

    def __init__(self):
        """Not yet implemented."""
        pass

    @abstractmethod
    def generate_competency(self, min_competency):
        """Generate and return random household competency level."""
        return random.uniform(min_competency, 1.0)

    @abstractmethod
    def generate_ambition(self, min_ambition):
        """Generate and return random household ambition level."""
        return random.uniform(min_ambition, 1.0)

    @abstractmethod
    def generate_position(self, environment):
        """Generate and return random household coordinate tuple."""
        nrows, ncols = environment.shape
        x_pos, y_pos = random.randint(0, ncols-1), random.randint(0, nrows-1)
        return (x_pos, y_pos)

    @abstractmethod
    def choose_claim_field(self, knowledge_ratio, num_workers, current_position, environment):
        """Not yet implemented."""
        knowledge_radius = knowledge_ratio*num_workers
        x_pos, y_pos = current_position
        x_field = x_pos + int(random.uniform(0, knowledge_radius))
        y_field = y_pos + int(random.uniform(0, knowledge_radius))
        # TODO: Create helper function that returns border if over border.
        return (x_field, y_field)

    @abstractmethod
    def relocate(self, knowledge_ratio, num_workers, current_position, environment):
        """Return relocation position tuple.

        Relocation position is within the household's knowledge_radius. The new
        position can't stray beyond the borders of the environment.
        """
        nrow, ncol = environment.shape
        x_pos, y_pos = current_position
        knowledge_radius = num_workers*knowledge_ratio
        new_x = x_pos + int(random.uniform(-knowledge_radius, knowledge_radius))
        new_y = y_pos + int(random.uniform(-knowledge_radius, knowledge_radius))
        if new_x < 0 or new_x > ncol-1 or new_y < 0 or new_y > nrow-1:
            return (x_pos, y_pos)
        else:
            return (new_x, new_y)
