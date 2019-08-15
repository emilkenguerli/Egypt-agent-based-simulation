import random

import numpy as np
import pandas as pd


class Household:
    """Represent communities or households in the neolithic era of ancient Egypt"

    This class encompasses all actions, interactions and attributes of an
    autonomous agent in the ABMS (Agent-based Model Simulation).
    """

    def __init__(self, model, id, num_workers, grain, generation_countdown, min_competency, min_ambition, rconfig, env):
        """Initialise household attributes upon object instantiation.

        Keyword arguments:
        model                -- model that defines the decisions made by the household
        id                   -- household identification number
        num_workers          -- size of household
        grain                -- current amount of grain held by household
        generation_countdown -- not implemented
        KNOWLEDGE_RATIO      -- knowledge_radius per household specified in pixels
        min_competency       -- generated competency between min_competency and 1
        min_ambition         -- generated ambition between min_ambition and 1
        env                  -- used to determine the household's starting position

        Set of attributes defines the state of the household at a specific point in
        time (generation).
        """
        self.KNOWLEDGE_RATIO = rconfig['knowledge_ratio'] # In pixels.
        self.CLAIM_RATIO = rconfig['claim_ratio']

        self.model = model
        self.id = id
        self.num_workers = num_workers
        self.grain = grain
        self.fields_owned = 0
        self.generation_countdown = generation_countdown
        self.competency = model.generate_competency(min_competency)
        self.ambition = model.generate_ambition(min_ambition)
        self.position = model.generate_position(env)
        self.columns = ['id','num_workers','grain','fields_owned','generation_countdown',
            'competency','ambition','x_pos','y_pos', 'knowledge_radius']


    def statistics(self):
        """Return dictionary of attribute information."""
        # TODO: more pythonic to use internal __dict__ attribute (possibly faster as well)
        x, y = self.position
        knowledge_radius = self.KNOWLEDGE_RATIO*self.num_workers
        data_dict = {'id':self.id, 'num_workers':self.num_workers, 'grain':self.grain, 'fields_owned':self.fields_owned,
            'generation_countdown':self.generation_countdown, 'competency':self.competency, 'ambition':self.ambition,
                'x_pos':x, 'y_pos':y, 'knowledge_radius':knowledge_radius}
        return data_dict

    def claim_fields(self, environment):
        """Not implemented."""
        claim_chance = random.random()
        if(claim_chance < self.ambition and self.num_workers > self.fields_owned):
            x_field, y_field = self.model.choose_claim_fields(self.KNOWLEDGE_RATIO, self.num_workers, self.position, environment)

            # y_max, x_max = environment.shape
            # if(y_field > 0 and x_field > 0 and y_field < y_max and x_field < x_max):
            #     claimed = environment.claim_map[y_field, x_field]
            #     fertile = environment.fertility_map[y_field, x_field]
            #     if not claimed and not fertile:
                    # environment.claim_map[y_field, x_field] = self.id

    def farm(self, environment):
        """Not implemented."""
        pass

    def consume_grain(self, environment):
        """Not implemented."""
        pass

    def storage_loss(self, environment):
        """Not implemented."""
        pass

    def relocate(self, environment):
        """Assign new position to household."""
        x, y = self.model.relocate(self.KNOWLEDGE_RATIO, self.num_workers, self.position, environment)
        self.position = (x, y)

    def get_grain(self):
        """Return current grain amount held by household."""
        return self.grain
