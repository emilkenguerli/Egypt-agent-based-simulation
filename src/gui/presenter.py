from tkinter import ttk
import tkinter as tk

import pandas as pd

from gui.frame_view import FrameView
from gui.user_view import UserView

class Presenter:
    """Retrieves and formats data for the FrameView and UserView.

    The presenter serves as a layer between the application layer and user
    interface. All interactions between the Simulation and the views of the
    project only occur through this class. The UserView and FrameView have no
    knowledge of the Simulation and vice versa. The FrameView and UserView are
    initialised in the presenter as per the MVP architectural pattern.

    Attributes:
        simulation: The singleton simulation object.
        columns: Attributes that make up the statistics of the simulation.
        frame_view: The singleton View object that is reponsible for viewing the
            simulation environment and the corresponding statistical graphs.
        root: Parameter for UserView instantiation.
        progress_var: Parameter for UserView instantiation.
        user_view: Main window of the application.
    """

    def __init__(self, simulation):
        """Initialise presenter attributes upon object instantiation."""
        self.simulation = simulation
        self.columns = simulation.households[0].columns
        self.frame_view = FrameView(self)
        self.root = tk.Tk()
        self.progress_var = tk.IntVar()
        self.user_view = UserView(self, self.progress_var, master=self.root)

    def start_application(self):
        """Initialises the main window of the application."""
        self.root.wm_title("Egypt Application")
        self.root.geometry("300x360")
        self.root.style = ttk.Style()
        self.root.style.theme_use("clam")
        self.root.mainloop()

    def simulate_year(self):
        """Runs a simulated year."""
        self.simulation.run_year_simulation(self)

    def statistics(self):
        """Aggregates and returns all households attributes as a pandas DataFrame."""
        df = pd.DataFrame(columns=self.columns)
        for household in self.simulation.households:
            row = household.statistics()
            df = df.append(row, ignore_index=True)
        return df

    def river_map(self):
        """Retrieves and returns river_map from the environment."""
        return self.simulation.environment.river_map

    def fertility_map(self):
        """Retrieves and returns fertility_map from the environment."""
        return self.simulation.environment.fertility_map

    def update(self):
        """Tells the frame_view to save the current simulation state as a frame."""
        self.frame_view.save_frame()

    def get_num_generations(self):
        """Retrieves and returns the number of generations in the simulation."""
        return self.simulation.num_generations

    def get_generation(self):
        """Retrieves and returns the current generation of the simulation."""
        return self.simulation.generation
