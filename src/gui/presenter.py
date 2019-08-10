import pandas as pd
from gui.view import View

class Presenter:
    """Retrieve and format data for the View."""

    def __init__(self, environment, households, num_generations):
        """Initialise presenter attributes upon object instantiation.

        Keyword arguments:
        environment         -- environment
        households          -- list of household objects
        num_generations     -- specifies the number of iterations in the simulation

        The presenter essentially serves as a layer between the application layer
        and user interface.
        """
        self.environment = environment
        self.households = households
        self.columns = households[0].columns
        # Assumes 'columns' attribute is the same for all households.
        self.num_generations = num_generations
        self.view = View(self)

    def statistics(self):
        """Convert and return household list as a pandas dataframe."""
        df = pd.DataFrame(columns=self.columns)
        for household in self.households:
            row = household.statistics()
            df = df.append(row, ignore_index=True)
        return df

    def update(self):
        """Tell view to save the current state of the simulation as a frame."""
        self.view.save_frame()

    def river_map(self):
        """Return river_map numpy array attribute of environment object."""
        return self.environment.river_map

    def fertility_map(self):
        """Return fertility_map numpy array attribute of environment object."""
        return self.environment.fertility_map
