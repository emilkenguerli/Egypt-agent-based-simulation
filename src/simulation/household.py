import math

import numpy as np


class Household:
    """Represent communities or households in the neolithic era of ancient Egypt"

    This class encompasses all actions, interactions and attributes of an
    autonomous agent in the ABMS (Agent-based Model Simulation).
    """

    def __init__(self, model, id, num_workers, grain, generation_countdown, min_competency, min_ambition, rconfig, env):
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

        self.model = model
        self.id = id
        self.num_workers = num_workers
        self.grain = grain
        self.fields_owned = 0
        self.generation_countdown = generation_countdown
        self.competency = model.generate_competency(min_competency)
        self.ambition = model.generate_ambition(min_ambition)
        self.position = model.generate_position(env)

        self.columns = ['id', 'num_workers', 'grain', 'fields_owned', 'generation_countdown',
            'competency', 'ambition', 'x_pos','y_pos', 'knowledge_radius']

    def statistics(self):
        """Return dictionary of attribute information."""
        # TODO: more pythonic to use internal __dict__ attribute (possibly faster as well)
        x_pos, y_pos = self.position
        knowledge_radius = self.KNOWLEDGE_RATIO*self.num_workers
        data_dict = {'id':self.id, 'num_workers':self.num_workers, 'grain':self.grain, 'fields_owned':self.fields_owned,
            'generation_countdown':self.generation_countdown, 'competency':self.competency, 'ambition':self.ambition,
                'x_pos':x_pos, 'y_pos':y_pos, 'knowledge_radius':knowledge_radius}
        return data_dict

    def claim_field(self, environment):
        """Not implemented."""
        field_coord = self.model.choose_claim_field(self.KNOWLEDGE_RATIO, self.num_workers, self.position, environment)
        available_area = self.CLAIM_RATIO * self.num_workers
        claimed_area = available_area * self.ambition
        claimed_field = (field_coord, available_area)
        self.claimed_field = claimed_field

    def farm(self, environment):
        """Not implemented."""
        field_coord, available_area = self.claimed_field
        x_field, y_field = field_coord
        sqrt_area = math.sqrt(available_area)
        claimed_area = math.floor(sqrt_area)**2
        # Converts the max_area of a claim field to a square set of pixels.
        # On average, the difference between max_area and area increases as the number of workers increase.
        # This is representative of increasing economies of scale (or inefficiencies that arise from an
        # increasing labour force).

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
        self.grain = self.grain + potential_harvest * self.competency

    def consume_grain(self, environment):
        """Not implemented."""
        pass

    def storage_loss(self, environment):
        """Not implemented."""
        pass

    def relocate(self, environment):
        """Assign new position to household."""
        new_x, new_y = self.model.relocate(self.KNOWLEDGE_RATIO, self.num_workers, self.position, environment)
        self.position = (new_x, new_y)
