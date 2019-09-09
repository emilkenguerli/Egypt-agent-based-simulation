"""Executes the application and contains the Simulation class.

Prior to the start of the simulation, the relevant start parameters are read in
and objects initialised.
"""
import math
import uuid
import time
import cProfile
import pstats
import io

import matplotlib.image as mpimg
import yaml

from simulation.environment import Environment
from gui.presenter import Presenter
from simulation.household import Household
from model.agent_model import AgentModel


class Simulation:
    """Drives the simulation of the agent-based model (ABM).

    The agents in the ABM are the Household objects whom interact with each
    other and the environment over the course of the simulation. It is important
    to note that the Simulation class is completely decoupled from the FrameView
    and UserView classes. All presentation logic is pushed to the Presenter
    singleton object, which is then utilised by the relevant Views.

    Attributes:
        households: List of Household objects.
        environment: Singleton object that encapsulates the features of the
            underlying landscape upon which the simulation takes place.
        num_generations: An integer that refers to the number of generations
            in the simulation.
    """


    def __init__(self, households, environment, num_generations):
        """Initialises simualtion attributes upon instantiation.

        Args:
            households: List of Household objects.
            environment: Singleton object that encapsulates the features of the
                underlying landscape upon which the simulation takes place.
            num_generations: An integer that refers to the number of generations
                in the simulation.
        """
        self.households = households
        self.environment = environment
        self.num_generations = num_generations
        self.generation = 0

    def run_year_simulation(self, presenter):
        """Runs the ancient egypt simulation for a year.

        The simulation updates the state of Simulation by a single year. A call
        to this method will only progress the simulation should the current year
        be less than the total number of years to be simulated. All households
        partake in a set of actions every generational tick, which affect both
        the landscape and its inhabitants (other households).

        Args:
            presenter: A singleton object that controls the flow of information
                to and from the relevant views.
        """
        if self.generation < self.num_generations or self.households:
            self.households.sort(key=lambda x: x.grain, reverse=True)
            for house in self.households:
                house.interaction = 0
                claimed_field = house.claim_field(self.environment)
                house.farm(claimed_field, self.environment)
                house.consume_grain()
                if house.num_workers <= 0:
                    self.households.remove(house)

            self.interact()
            presenter.update()
            for house in self.households:
                house.grow()
                house.generational_changeover()
                house.relocate(self.environment)

            self.environment.flood(self.generation)
            self.generation += 1

    def interact(self):
        """Initiates interactions between all intersecting households."""
        remaining = []
        for index_1 in range(len(self.households)):
            for index_2 in range(index_1, len(self.households)):
                house_1 = self.households[index_1]
                house_2 = self.households[index_2]
                if house_1.id is house_2.id:
                    continue
                intersection = self.intersect(house_1, house_2)
                if house_1.num_workers > 0 and house_2.num_workers > 0 and intersection:
                    self.interaction(house_1, house_2)
            if house_1.num_workers > 0:
                remaining.append(house_1)
        self.households = remaining

    def intersect(self, house_1, house_2):
        """Determines whether two households intersect.

        Args:
            house_1: Household object.
            house_2: Household object.

        Returns:
            A boolean expression indicating whether an intersection exists or
            not.
        """
        x_1, y_1 = house_1.position
        x_2, y_2 = house_2.position
        square_dist = (x_1 - x_2)**2 + (y_1 - y_2)**2
        distance = math.sqrt(square_dist)
        r_1 = house_1.knowledge_radius
        r_2 = house_2.knowledge_radius
        return distance <= (r_1 + r_2)

    def interaction(self, house_1, house_2):
        """Defines game theory interaction between two households.

        Collaboration only occurs if both households agree to collaborate but
        each households is free to plunder regardless of the other household's
        strategy.

        Args:
            house_1: Household object.
            house_2: Household object.
        """
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
    """Loads and returns the global configuration dictionary.

    Args:
        config_file: Path to a yaml configuration file.

    Returns:
        A dictionary where the keys are simulation parameters and the
        corresponding values are user-specified inputs to the simulation.
    """
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def setup_map(map_file, myLogger):
    """Reads and returns a numpy array its shape from a picture file.

    Args:
        map_file: Path to a map picture file.

    Returns:
        A tuple containing a numpy.ndarray and a shape tuple. Each value in the
        array represents a pixel in the corresponding map picture file. The
        supplied images are grayscale and, hence, the pixel values will be
        between 0.0 and 1.0.
    """

    myLogger.info('Reading in map image into a numy array')
    np_map = mpimg.imread(map_file)
    shape = np_map.shape
    return np_map, shape


def setup_households(env, var_config, const_config):
    """Creates and returns a list of household objects.

    Args:
        var_config: Path to a config file containing simulation parameters that
            will vary throughout the simulation.
        const_config: Path to a config file containing simulation parameters
            that remain constant throughout the simulation.

    Returns:
        A list of Household objects.
    """
    households = []
    for _ in range(var_config['num_households']):
        model = AgentModel()
        id = uuid.uuid1()
        household_config = var_config['households']
        num_workers = household_config['num_workers']
        grain = household_config['grain']
        worker_capability = household_config['worker_capability']
        min_competency = household_config['min_competency']
        min_ambition = household_config['min_ambition']
        household = Household(model, id, num_workers, grain, worker_capability,
                              min_competency, min_ambition, const_config, env)
        households.append(household)
    return households

def load_config(config_file):
    """Loads and returns the global configuration dictionary.

    Args:
        config_file: Path to a yaml configuration file.

    Returns:
        A dictionary where the keys are simulation parameters and the
        corresponding values are user-specified inputs to the simulation.
    """
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError:
            myLogger.exception('Failed to parse config')


def main():

    var_config = load_config('../var_config.yml')
    const_config = load_config('../const_config.yml')
    river_map, map_shape = setup_map('../../resources/maps/river_map.png')
    fertility_map, map_shape = setup_map('../../resources/maps/fertility_map.png')

    num_generations = const_config['num_generations']
    environment = Environment(river_map, fertility_map, map_shape, const_config)
    households = setup_households(environment, var_config, const_config)
    simulation = Simulation(households, environment, num_generations)
    presenter = Presenter(simulation)

    pr = cProfile.Profile()
    pr.enable()

    presenter.start_application()

    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
    ps.print_stats()

    with open('../../logs/profiling/profile.txt', 'w+') as f:
        f.write(s.getvalue())


if __name__ == "__main__":
    main()