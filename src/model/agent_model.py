from simulation.model_interface import AbstractModel


class AgentModel(AbstractModel):
    """Agent model controls household decision-making.

    Keyword arguments:
    AbstractModel -- superclass (abstract base class)

    Each model instance serves as the decision-making core of a particular
    household. It contains the memory of previous generations and past decisions.
    Each method represents a possible decision, thus giving The associated
    household its autonomy.

    Contains methods that represent decision-making of higher complexity."""

    def __init__(self):
        """Not implemented."""
        pass

    def generate_competency(self, min_competency):
        """Extend superclass method."""
        return super().generate_competency(min_competency)

    def generate_ambition(self, min_ambition):
        """Extend superclass method."""
        return super().generate_ambition(min_ambition)

    def generate_position(self, environment):
        """Extend superclass method.

        Additional functionality includes the repeated generation of a position
        should the generated position contain a river pixel.
        """
        x, y = super().generate_position(environment)
        river_map = environment.river_map
        while river_map[y, x]:
            x, y = super().generate_position(environment)
        return (x, y)

    def choose_claim_fields(self, knowledge_ratio, num_workers, current_position, environment):
        """Not implemented."""
        return super().choose_claim_fields(num_workers, knowledge_ratio, current_position, environment)

    def relocate(self, knowledge_ratio, num_workers, current_position, environment):
        """Extend superclass method."""
        river_map = environment.river_map
        x, y = super().relocate(num_workers, knowledge_ratio, current_position, environment)
        if not river_map[y, x]:
            return (x, y)
        else:
            return current_position
