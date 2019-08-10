import random

import numpy as np
import pandas as pd


class Household:
    """Represent communities or households in the neolithic era of ancient Egypt"

    This class encompasses all actions, interactions and attributes of an
    autonomous agent in the ABMS (Agent-based Model Simulation).
    """

    def __init__(self, model, id, num_workers, grain, generation_countdown, knowledge_ratio, min_competency, min_ambition, env):
        """Initialise household attributes upon object instantiation.

        Keyword arguments:
        model                -- model that defines the decisions made by the household
        id                   -- household identification number
        num_workers          -- size of household
        grain                -- current amount of grain held by household
        generation_countdown -- not implemented
        knowledge_ratio      -- knowledge_radius per household specified in pixels
        min_competency       -- generated competency between min_competency and 1
        min_ambition         -- generated ambition between min_ambition and 1
        env                  -- used to determine the household's starting position

        Set of attributes defines the state of the household at a specific point in
        time (generation).
        """
        self.__model = model
        self.__id = id
        self.__num_workers = num_workers
        self.__grain = grain
        self.__fields_owned = 0
        self.__generation_countdown = generation_countdown
        self.__knowledge_ratio = knowledge_ratio # In pixels.
        self.__competency = model.generate_competency(min_competency)
        self.__ambition = model.generate_ambition(min_ambition)
        self.__position = model.generate_position(env)
        self.columns = ['id','num_workers','grain','fields_owned','generation_countdown','knowledge_ratio','competency','ambition','x_pos','y_pos']

    def statistics(self):
        """Return dictionary of attribute information."""
        x, y = self.__position
        data_dict = {'id':self.__id, 'num_workers':self.__num_workers, 'grain':self.__grain, 'fields_owned':self.__fields_owned,
            'generation_countdown':self.__generation_countdown, 'knowledge_ratio':self.__knowledge_ratio, 'competency':self.__competency, 'ambition':self.__ambition, 'x_pos':x, 'y_pos':y}
        return data_dict

    def claim_fields(self, environment):
        """Not implemented."""
        claim_chance = random.random()
        if(claim_chance < self.__ambition and self.__num_workers > self.__fields_owned):
            knowledge_radius = self.__knowledge_ratio*self.__num_workers
            x_pos, y_pos = self.__position

            x_field = x_pos + int(random.uniform(0, knowledge_radius)) # Create helper function that returns border if over border.
            y_field = y_pos + int(random.uniform(0, knowledge_radius))

            y_max, x_max = environment.shape
            if(y_field > 0 and x_field > 0 and y_field < y_max and x_field < x_max):
                claimed = environment.claim_map[y_field, x_field]
                fertile = environment.fertility_map[y_field, x_field]
                if not claimed and not fertile:
                    environment.claim_map[y_field, x_field] = self.__id

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
        x, y = self.__model.relocate(self, environment)
        self.__position = (x, y)

    def get_grain(self):
        """Return current grain amount held by household."""
        return self.__grain
