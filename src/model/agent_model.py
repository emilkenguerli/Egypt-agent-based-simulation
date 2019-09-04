"""
Todo:
    * Memory needs to be incorporated into this class. Each AgentModel instance
        would need to record the statistics of their household as the Simulation
        progresses. The various actions taken would also need to be recorded.
        The memory stored in the AgentModel instances need only be a pandas
        DataFrame.
    * Incorporate machine learning in which each AgentModel instance makes
        decisions or undertakes actions based on its Memory.
"""

from simulation.model_interface import AbstractModel


class AgentModel(AbstractModel):
    """Agent model controls household decision-making.

    Each model instance serves as the decision-making core of a particular
    household. Each method represents a possible decision, thus giving the
    household its autonomy.
    """

    def generate_competency(self, min_competency):
        """Overrides superclass method."""
        return super().generate_competency(min_competency)

    def generate_ambition(self, min_ambition):
        """Overrides superclass method."""
        return super().generate_ambition(min_ambition)

    def generate_position(self, environment):
        """Overrides superclass method.

        Extended functionality includes the repeated generation of a position
        should the generated position contain a river pixel.
        """
        x, y = super().generate_position(environment)
        river_map = environment.river_map
        while river_map[y, x]:
            x, y = super().generate_position(environment)
        return (x, y)

    def choose_claim_field(self, knowledge_radius, current_position, environment):
        """Overrides superclass method."""
        return super().choose_claim_field(knowledge_radius, current_position, environment)

    def relocate(self, knowledge_radius, current_position, environment):
        """Overrides superclass method.

        Extended functionality includes the repeated generation of a position
        should the generated position contain a river pixel.
        """
        river_map = environment.river_map
        x, y = super().relocate(knowledge_radius, current_position, environment)
        if not river_map[y, x]:
            return (x, y)
        else:
            return current_position

    def strategy(self, household_id):
        """Overrides superclass method."""
        return super().strategy(household_id)
