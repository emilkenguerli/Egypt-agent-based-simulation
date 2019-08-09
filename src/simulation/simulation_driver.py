import logging

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import yaml

from environment import Environment
from gui.presenter import Presenter
from household import Household
from model.agent_model import AgentModel


def setup_map(map_file):
    map = mpimg.imread(map_file)
    shape = map.shape
    return map, shape


def setup_households(env, config):
    households = []
    for id in range(config['num_households']): # Will currently illicit strange behaviour when claiming fields
        model = AgentModel()
        household_config = config['households']
        num_workers = household_config['num_workers']
        grain = household_config['grain']
        generation_countdown = household_config['generation_countdown']
        knowledge_ratio = household_config['knowledge_ratio']
        min_competency = household_config['min_competency']
        min_ambition = household_config['min_ambition']
        household = Household(model, id, num_workers, grain, generation_countdown, knowledge_ratio, min_competency, min_ambition, env)
        households.append(household)
    return households


def load_config(config_file):
    """Load and return the global configuration file."""
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def run_simulation(presenter):
    households = presenter.households
    env = presenter.environment
    while presenter.num_generations > 0:
        if not households:
            break
        households.sort(key=lambda x: x.get_grain(), reverse=True)
        for house in households:
            house.claim_fields(env)
            house.farm(env)
            house.relocate(env)
        presenter.update()
        presenter.num_generations -= 1
    presenter.finish()


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(100)

    river_map, shape = setup_map('../../resources/maps/river_map.png')
    fertility_map, shape = setup_map('../../resources/maps/fertility_map.png')
    config = load_config('../config.yml')
    num_generations = config['num_generations']
    env = Environment(river_map, fertility_map, shape)
    households = setup_households(env, config)
    presenter = Presenter(env, households, num_generations)
    run_simulation(presenter)
