from threading import Thread
from tkinter import ttk
import tkinter as tk

import pandas as pd
from gui.frame_view import FrameView
from gui.user_view import UserView

class Presenter:
    """Retrieve and format data for the FrameView."""

    def __init__(self, simulation):
        """Initialise presenter attributes upon object instantiation.

        Keyword arguments:
        environment         -- environment
        households          -- list of household objects
        num_generations     -- specifies the number of iterations in the simulation

        The presenter essentially serves as a layer between the application layer
        and user interface.
        """
        self.simulation = simulation
        self.columns = simulation.households[0].columns
        self.frame_view = FrameView(self)
        self.root = tk.Tk()
        self.progress_var = tk.IntVar()
        self.user_view = UserView(self, self.progress_var, master=self.root)
        # self.sim_thread = Thread(target=self.simulation.run_simulation, args=(self,))

    def start_application(self):
        self.root.wm_title("Egypt Simulation")
        self.root.geometry("250x290")
        self.root.style = ttk.Style()
        self.root.style.theme_use("clam")
        # self.root.after(0, self.progress)
        self.root.mainloop()

    def start_simulation(self):
        self.simulation.run_simulation(self)

    def statistics(self):
        """Convert and return household list as a pandas dataframe."""
        df = pd.DataFrame(columns=self.columns)
        for household in self.simulation.households:
            row = household.statistics()
            df = df.append(row, ignore_index=True)
        return df

    def river_map(self):
        """Return river_map numpy array attribute of environment object."""
        return self.simulation.environment.river_map

    def fertility_map(self):
        """Return fertility_map numpy array attribute of environment object."""
        return self.simulation.environment.fertility_map

    def update(self):
        """Tell frame view to save the current state of the simulation as a frame."""
        self.frame_view.save_frame()

    def get_num_generations(self):
        return self.simulation.num_generations

    def get_generation(self):
        return self.simulation.generation
