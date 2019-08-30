import math
from threading import Thread
import uuid

import matplotlib.image as mpimg
import yaml

from environment import Environment
from gui.presenter import Presenter
from household import Household
from model.agent_model import AgentModel


class Simulation:
    def __init__(self, households, environment, num_generations):
        self.households = households
        self.environment = environment
        self.num_generations = num_generations
        self.generation = 0

    def run_simulation(self, presenter):
        """Run the ancient egypt simulation.

        Keyword arguments:
        presenter -- enables communication between the model and view of the simulation

        All households partake in a set of decisions every generational tick.
        External factors affect both the landscape and its populous.
        """

        while self.generation < self.num_generations:
            if not self.households:
                break
            presenter.update()
            self.households.sort(key=lambda x: x.grain, reverse=True)
            for house in self.households:
                house.interaction = 0
                claimed_field = house.claim_field(self.environment)
                house.farm(claimed_field, self.environment)
                house.consume_grain()
                if(house.num_workers <= 0):
                    self.households.remove(house)
                house.grow()
                house.relocate(self.environment)
            self.interact()
            self.generation += 1

    def interact(self):
        num_households = len(self.households)
        for index_1 in range(num_households):
            for index_2 in range(index_1 + 1, num_households):
                house_1 = self.households[index_1]
                house_2 = self.households[index_2]
                # FIXME: IndexError: list index out of range
                if self.intersect(house_1, house_2):
                    self.interaction(house_1, house_2)
                    if house_1.num_workers <= 0:
                        self.households.remove(house_1)
                        index_1 -= 1
                    if house_2.num_workers <= 0:
                        self.households.remove(house_2)
                        index_2 -= 1

    def intersect(self, house_1, house_2):
        x_1, y_1 = house_1.position
        x_2, y_2 = house_2.position
        square_dist = (x_1 - x_2)**2 + (y_1 - y_2)**2
        distance = math.sqrt(square_dist)
        r_1 = house_1.knowledge_radius
        r_2 = house_2.knowledge_radius
        if(distance <= (r_1 + r_2)):
            return True
        else:
            return False

    def interaction(self, house_1, house_2):
        action_1 = house_1.strategy(house_2)
        action_2 = house_2.strategy(house_1)
        if action_1 < 0 and action_2 < 0:
            house_1.plunder(house_2); house_2.plunder(house_1)
        elif action_1 < 0 and action_2 >= 0:
            house_1.plunder(house_2)
        elif action_1 >= 0 and action_2 < 0:
            house_2.plunder(house_1)
        elif action_1 > 0 and action_2 > 0:
            house_1.collaborate(house_2); house_2.collaborate(house_1)


def load_config(config_file):
    """Load and return the global configuration dictionary."""
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


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


if __name__ == "__main__":
    write_config = load_config('../w_config.yml')
    read_config = load_config('../r_config.yml')
    river_map, map_shape = setup_map('../../resources/maps/river_map.png')
    fertility_map, map_shape = setup_map('../../resources/maps/fertility_map.png')

    num_generations = write_config['num_generations']
    environment = Environment(river_map, fertility_map, map_shape)
    households = setup_households(environment, write_config, read_config)
    simulation = Simulation(households, environment, num_generations)
    presenter = Presenter(simulation)

    presenter.start_application()



    # run_simulation(presenter)
