from simulation.model_interface import AbstractModel

# all decisions controlled by this class.

class AgentModel(AbstractModel):
    def __init__(self):
        pass

    def generate_competency(self, min_competency):
        return super().generate_competency(min_competency)

    def generate_ambition(self, min_ambition):
        return super().generate_ambition(min_ambition)

    def generate_position(self, environment):
        x, y = super().generate_position(environment)
        river_map = environment.river_map
        while river_map[y, x]:
            # Assumes river pixels have a value of 1.
            x, y = super().generate_position(environment)
        return (x, y)

    def choose_fields(self, environment):
        pass

    def relocate(self, household, environment):
        return super().relocate(household, environment)
