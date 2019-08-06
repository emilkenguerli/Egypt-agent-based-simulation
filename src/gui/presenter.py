import pandas as pd
from gui.view import UserInterface

class Presenter:
    """ """

    def __init__(self, environment, households, num_generations):
        self.environment = environment
        self.households = households
        self.columns = households[0].columns
        # Assumes 'columns' attribute is the same for all households.
        self.num_generations = num_generations
        self.ui = UserInterface(self)
        self.ui.start()


    def statistics(self):
        df = pd.DataFrame(columns=self.columns)
        for household in self.households:
            row = household.statistics()
            df = df.append(row, ignore_index=True)
        print(df)
        return df

    def map(self):
        return self.environment.map
