import pandas as pd
from gui.view import View

class Presenter:
    """ """

    def __init__(self, environment, households, num_generations):
        self.environment = environment
        self.households = households
        self.columns = households[0].columns
        # Assumes 'columns' attribute is the same for all households.
        self.num_generations = num_generations
        self.view = View(self)

    def statistics(self):
        df = pd.DataFrame(columns=self.columns)
        for household in self.households:
            row = household.statistics()
            df = df.append(row, ignore_index=True)
        return df

    def update(self):
        self.view.save_frame()

    def river_map(self):
        return self.environment.river_map

    def fertility_map(self):
        return self.environment.fertility_map
