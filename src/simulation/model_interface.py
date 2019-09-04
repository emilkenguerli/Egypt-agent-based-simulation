from abc import ABC, abstractmethod
import random


class AbstractModel(ABC):
    """Implements a simple model for household decision-making.

    AbstractModel inherits ABC (Abstract Base Class), which provides the
    @abstractmethod decorator. The AbstractModel must be inherited by the
    AgentModel, which must override all abstract methods of the AbstractModel
    class.
    """

    @abstractmethod
    def generate_competency(self, min_competency):
        """Generates and returns random household competency level.

        Args:
            min_competency: Minimum competency of the household upon household
                initialisation.

        Returns:
            A random float between min_competency and 1.0.
        """
        return random.uniform(min_competency, 1.0)

    @abstractmethod
    def generate_ambition(self, min_ambition):
        """Generates and returns random household ambition level.

        Args:
            min_ambition: Minimum ambition of the household upon household
                initialisation.

        Returns:
            A random float between min_ambition and 1.0.
        """
        return random.uniform(min_ambition, 1.0)

    @abstractmethod
    def generate_position(self, environment):
        """Generates and returns a random household start coordinate.

        Args:
            environment: Simulation landscape.

        Returns:
            A tuple of random x and y positions within the boundary defined by
            the environment.
        """
        nrows, ncols = environment.shape
        x_pos, y_pos = random.randint(0, ncols-1), random.randint(0, nrows-1)
        return (x_pos, y_pos)

    @abstractmethod
    def choose_claim_field(self, knowledge_radius, current_position, environment):
        """Chooses and returns a position to be the center of a claimed field.

        Args:
            knowledge_radius: The radius of the circle whose area defines the
                regions in the environment that the relevant household is aware
                of.
            current_position: Position of the center of the circle that defines
                the households knowledge_radius.
            environment: Simulation landscape.

        Returns:
            A tuple of random x and y positions within the boundary defined by
            the household's knowledge_radius.
        """
        x_pos, y_pos = current_position
        x_field = x_pos + int(random.uniform(0, knowledge_radius))
        y_field = y_pos + int(random.uniform(0, knowledge_radius))
        return (x_field, y_field)

    @abstractmethod
    def relocate(self, knowledge_radius, current_position, environment):
        """Returns relocation position.

        Args:
            knowledge_radius: The radius of the circle whose area defines the
                regions in the environment that the relevant household is aware
                of.
            current_position: Position of the center of the circle that defines
                the households knowledge_radius.
            environment: Simulation landscape.

        Returns:
            A tuple of random x and y positions within the boundary defined by
            the household's knowledge_radius.
        """
        nrow, ncol = environment.shape
        x_pos, y_pos = current_position
        new_x = x_pos + int(random.uniform(-knowledge_radius, knowledge_radius))
        new_y = y_pos + int(random.uniform(-knowledge_radius, knowledge_radius))
        if new_x < 0 or new_x > ncol-1 or new_y < 0 or new_y > nrow-1:
            return (x_pos, y_pos)
        else:
            return (new_x, new_y)

    @abstractmethod
    def strategy(self, household_id):
        """Returns the strategy to be undertaken during a household interaction.

        Args:
            household_id: UUID that identifies the household currently being
                interacted with. The main idea is for the household's decision
                making model (AgentModel) to remember any previous interactions
                with this household and act accordingly

        Returns:
            An integer in the set {-1, 0, 1} which indicate malice, indifference
            and benevolence respectively.
        """
        return random.randint(-1, 1)
