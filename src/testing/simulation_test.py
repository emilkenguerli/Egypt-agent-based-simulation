from unittest import TestCase, main

import numpy as np

from simulation.environment import Environment
from simulation.household import Household
from simulation.simulation_driver import Simulation
from simulation import simulation_driver

class SimulationClassTest(TestCase):

    def setUp(self):
        var_config = simulation_driver.load_config('../var_config.yml')
        const_config = simulation_driver.load_config('../const_config.yml')
        river_map, map_shape = simulation_driver.setup_map('../../resources/maps/river_map.png')
        fertility_map, map_shape = simulation_driver.setup_map('../../resources/maps/fertility_map.png')

        num_generations = const_config['num_generations']
        self.environment = Environment(river_map, fertility_map, map_shape, const_config)
        self.households = simulation_driver.setup_households(self.environment, var_config, const_config)
        self.simulation = Simulation(self.households, self.environment, num_generations)

    def test_household_harvest(self):
        for _ in range(100):
            for house in self.households:
                claimed_field = house.claim_field(self.environment)
                field_coord, claimed_area = claimed_field
                x_pos, y_pos = field_coord
                row, col = self.environment.shape
                house.farm(claimed_field, self.environment)
                assert x_pos <= col
                assert y_pos <= row
                assert house.grain >= 0

    def test_household_consume_grain(self):
        for _ in range(100):
            for house in self.households:
                claimed_field = house.claim_field(self.environment)
                house.farm(claimed_field, self.environment)
                house.consume_grain()
                assert house.grain >= 0
                assert house.num_workers >= 0

    def test_household_strategy(self):
        interaction_set = {-1, 0 , 1}
        for house_1 in self.households:
            for house_2 in self.households:
                if house_1.id is not house_2.id:
                    interaction = house_1.strategy(house_2)
                    assert (interaction in interaction_set)

    def test_household_collaborate(self):
        for house_1 in self.households:
            for house_2 in self.households:
                if house_1.id is not house_2.id:
                    house_1.collaborate(house_2)
                    assert house_1.worker_capability >= 0

    def test_household_plunder(self):
        for house_1 in self.households:
            for house_2 in self.households:
                if house_1.id is not house_2.id:
                    house_1.plunder(house_2)
                    assert house_2.grain >= 0
                    assert house_2.num_workers >=0

    def test_household_generational_changeover(self):
        for _ in range(100):
            for house in self.households:
                house.generational_changeover()
                assert house.competency >= 0 and house.competency <= 1
                assert house.ambition >= 0 and house.ambition <= 1
                assert house.worker_capability >= 0

    def test_environment_flood(self):
        self.environment.FLOOD_FREQ = 1
        for generation in range(100):
            original_fertility_map = np.copy(self.environment.fertility_map)
            for house in self.households:
                claimed_field = house.claim_field(self.environment)
                house.farm(claimed_field, self.environment)
            assert not np.array_equal(self.environment.fertility_map, original_fertility_map)
            self.environment.flood(generation)
            assert np.array_equal(self.environment.fertility_map, original_fertility_map)


class SimulationIntegrationTest(TestCase):

    def setUp(self):
        var_config = simulation_driver.load_config('../var_config.yml')
        const_config = simulation_driver.load_config('../const_config.yml')
        river_map, map_shape = simulation_driver.setup_map('../../resources/maps/river_map.png')
        fertility_map, map_shape = simulation_driver.setup_map('../../resources/maps/fertility_map.png')

        num_generations = const_config['num_generations']
        self.environment = Environment(river_map, fertility_map, map_shape, const_config)
        self.households = simulation_driver.setup_households(self.environment, var_config, const_config)
        self.simulation = Simulation(self.households, self.environment, num_generations)

    def test_main_simulation(self):
        class Presenter:
            def __init__(self, households):
                self.households = households
            def update(self):
                for house in self.households:
                    assert house.competency >= 0 and house.competency <= 1
                    assert house.ambition >= 0 and house.ambition <= 1
                    assert house.worker_capability >= 0
                    assert house.grain >= 0

        presenter = Presenter(self.households)
        for _ in range(1000):
            self.simulation.run_year_simulation(presenter)

if __name__ == "__main__":
    main()
