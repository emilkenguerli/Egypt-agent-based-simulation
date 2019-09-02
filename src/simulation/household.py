import math
import random
import statistics

import sys

class Household:
    """Represent communities or households in the neolithic era of ancient Egypt"

    This class encompasses all actions, interactions and attributes of an
    autonomous agent in the ABMS (Agent-based Model Simulation).
    """

    def __init__(self, model, id, num_workers, grain, min_competency,
                        min_ambition, rconfig, env):
        """Initialise household attributes upon object instantiation.

        Keyword arguments:
        KNOWLEDGE_RATIO      -- knowledge_radius per household specified in pixels
        model                -- model that defines the decisions made by the household
        id                   -- household identification number
        num_workers          -- size of household
        grain                -- current amount of grain held by household
        generation_countdown -- not implemented
        min_competency       -- generated competency between min_competency and 1
        min_ambition         -- generated ambition between min_ambition and 1
        env                  -- used to determine the household's starting position

        Set of attributes defines the state of the household at a specific point in
        time (generation).
        """
        self.KNOWLEDGE_RATIO = rconfig['knowledge_ratio'] # In pixels.
        self.CLAIM_RATIO = rconfig['claim_ratio']
        self.MAX_POTENTIAL_YIELD = rconfig['maximum_potential_yield']
        self.WORKER_CAPABILITY = rconfig['worker_capability']
        self.WORKER_APPETITE = rconfig['worker_appetite']
        self.GROWTH_RATE = rconfig['growth_rate']
        self.GENERATIONAL_VARIANCE = rconfig['generational_variance']

        self.model = model
        self.id = id
        self.num_workers = num_workers
        self.grain = grain
        self.fields_owned = 0
        self.interaction = 0
        self.competency = model.generate_competency(min_competency)
        self.ambition = model.generate_ambition(min_ambition)
        self.position = model.generate_position(env)

        self.columns = ['id', 'num_workers', 'grain', 'fields_owned', 'interaction',
                    'competency', 'ambition']

    @property
    def knowledge_radius(self):
        return self.KNOWLEDGE_RATIO * self.num_workers

    def statistics(self):
        """Return dictionary of attribute information."""
        x_pos, y_pos = self.position
        data_dict = {'x_pos':x_pos, 'y_pos':y_pos, 'knowledge_radius': self.knowledge_radius}
        for attr, value in self.__dict__.items():
            if attr in self.columns:
                data_dict[attr] = value
        return data_dict

    def claim_field(self, environment):
        """Not implemented."""
        field_coord = self.model.choose_claim_field(self.knowledge_radius, self.position, environment)
        available_area = self.CLAIM_RATIO * self.num_workers
        claimed_area = available_area * self.ambition
        claimed_field = (field_coord, claimed_area)
        return claimed_field

    def farm(self, claimed_field, environment):
        """Not implemented."""
        field_coord, available_area = claimed_field
        x_field, y_field = field_coord
        sqrt_area = math.sqrt(available_area)

        nrows, ncols = environment.shape
        diff = int(sqrt_area/2)
        x_start = max(0, x_field - diff)
        y_start = max(0, y_field - diff)
        x_end = min(ncols - 1, x_field + diff)
        y_end = min(nrows - 1, y_field + diff)
        fertility = environment.fertility_map[y_start:y_end, x_start:x_end]

        field = fertility * self.MAX_POTENTIAL_YIELD
        available_harvest = field.sum()
        workers_capability = self.num_workers * self.WORKER_CAPABILITY
        potential_harvest = min(available_harvest, workers_capability)
        harvest = potential_harvest * self.competency
        if available_harvest:
            percentage_unharvested = (available_harvest - harvest) / available_harvest
            fertility = fertility * percentage_unharvested
            environment.fertility_map[y_start:y_end, x_start:x_end] = fertility
        self.grain = self.grain + harvest

    def consume_grain(self):
        """Not implemented."""
        self.grain = self.grain - self.num_workers * self.WORKER_APPETITE
        if(self.grain < 0):
            resiliency = self.competency * self.ambition
            negative_workers = (self.grain / self.WORKER_APPETITE) * (1 - resiliency)
            self.num_workers += math.floor(negative_workers)
            self.grain = 0

    def grow(self):
        increase = self.num_workers * self.GROWTH_RATE
        new_workers = math.floor(increase)
        fraction = increase - new_workers
        if(random.random() < fraction):
            new_workers += 1
        self.num_workers += new_workers

    def relocate(self, environment):
        """Assign new position to household."""
        new_x, new_y = self.model.relocate(self.knowledge_radius, self.position, environment)
        self.position = (new_x, new_y)

    def strategy(self, household):
        self.interaction = self.model.strategy(household.id)
        return self.interaction

    def plunder(self, household):
        total_workers = self.num_workers + household.num_workers
        capability = statistics.mean((self.num_workers / total_workers, self.ambition, self.competency))
        rival_capability = statistics.mean((household.num_workers / total_workers, household.ambition, household.competency))
        plunder_probability = capability / (capability + rival_capability)
        plunder = random.random()
        if plunder < plunder_probability:
            stolen_grain = plunder * household.grain
            stolen_workers = math.ceil(plunder * household.num_workers)
            household.grain -= stolen_grain
            self.grain += stolen_grain
            household.num_workers -= stolen_workers
            self.num_workers += stolen_workers

    def collaborate(self, household):
        total_workers = self.num_workers + household.num_workers
        capability = statistics.mean((self.num_workers / total_workers, self.ambition, self.competency))
        other_capability = statistics.mean((household.num_workers / total_workers, household.ambition, household.competency))
        collab_probability = capability / (capability + other_capability)
        collab = random.random()
        if collab < collab_probability:
            trade = collab * household.grain
            worker_efficiency = math.floor(collab * household.num_workers)
            self.grain += trade
            self.num_workers += worker_efficiency

    def generational_changeover(self):
        self.competency += self.attribute_change(self.competency)
        self.ambition += self.attribute_change(self.ambition)
        assert(self.competency > 0 and self.competency < 1)
        assert(self.ambition > 0 and self.ambition < 1)


    def attribute_change(self, attr_value):
        variance = random.uniform(0, self.GENERATIONAL_VARIANCE)
        inc_chance = random.random()
        if inc_chance >= 0.5:
            return (1 - attr_value) * variance
        else:
            return 0 - (attr_value - 0) * variance
