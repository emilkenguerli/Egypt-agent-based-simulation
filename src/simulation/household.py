import random

import numpy as np
import pandas as pd


class Household:
    """ """

    def __init__(self, model, id, num_workers, grain, generation_countdown, knowledge_ratio, min_competency, min_ambition, env):
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
        x, y = self.__position
        data_dict = {'id':self.__id, 'num_workers':self.__num_workers, 'grain':self.__grain, 'fields_owned':self.__fields_owned,
            'generation_countdown':self.__generation_countdown, 'knowledge_ratio':self.__knowledge_ratio, 'competency':self.__competency, 'ambition':self.__ambition, 'x_pos':x, 'y_pos':y}
        return data_dict

    def claim_fields(self, environment):
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
        pass

    def consume_grain(self, environment):
        pass

    def storage_loss(self, environment):
        pass

    def get_grain(self):
        return self.__grain
