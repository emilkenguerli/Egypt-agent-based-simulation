import uuid

import matplotlib.image as mpimg
import yaml

from environment import Environment
from gui.presenter import Presenter
from household import Household
from model.agent_model import AgentModel


def setup_map(map_file):
    """Read and return a numpy array along with its shape.

    Keyword arguments:
    map_file -- path to map image
    """
    np_map = mpimg.imread(map_file)
    shape = np_map.shape
    return np_map, shape


def setup_households(env, w_config, r_config):
    """Create and return a list of household objects."""
    households = []
    for _ in range(w_config['num_households']):
        model = AgentModel()
        id = uuid.uuid1()
        household_config = w_config['households']
        num_workers = household_config['num_workers']
        grain = household_config['grain']
        generation_countdown = household_config['generation_countdown']
        min_competency = household_config['min_competency']
        min_ambition = household_config['min_ambition']
        household = Household(model, id, num_workers, grain, generation_countdown,
                              min_competency, min_ambition, r_config, env)
        households.append(household)
    return households


def load_config(config_file):
    """Load and return the global configuration dictionary."""
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def run_simulation(presenter):
    """Run the ancient egypt simulation.

    Keyword arguments:
    presenter -- enables communication between the model and view of the simulation

    All households partake in a set of decisions every generational tick.
    External factors affect both the landscape and its populous.
    """
    households = presenter.households
    env = presenter.environment
    while presenter.num_generations > 0:
        if not households:
            break
        households.sort(key=lambda x: x.grain, reverse=True)
        for house in households:
            claimed_field = house.claim_field(env)
            house.farm(claimed_field, env)
            house.consume_grain()
            if(house.num_workers <= 0):
                households.remove(house)
            house.grow()
            house.relocate(env)
        presenter.update()
        presenter.num_generations -= 1


if __name__ == "__main__":
    river_map, map_shape = setup_map('../../resources/maps/river_map.png')
    fertility_map, map_shape = setup_map('../../resources/maps/fertility_map.png')
    write_config = load_config('../w_config.yml')
    read_config = load_config('../r_config.yml')
    num_generations = write_config['num_generations']
    environment = Environment(river_map, fertility_map, map_shape)
    households = setup_households(environment, write_config, read_config)
    presenter = Presenter(environment, households, num_generations)
    run_simulation(presenter)
