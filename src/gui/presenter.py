from tkinter import ttk
import tkinter as tk

import pandas as pd
from gui.frame_view import FrameView
from gui.user_view import UserView

class Presenter:
    """Retrieve and format data for the FrameView."""

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
        self.num_generations = num_generations
        self.generation = 0
        self.frame_view = FrameView(self)

        self.root = tk.Tk()
        self.progress_var = tk.IntVar()
        self.user_view = UserView(self, self.progress_var, master=self.root)

    def start_application(self):
        # sim_thread = Thread(target=run_simulation, args=(presenter,))
        # sim_thread.start()
        self.run_user_view()
        # sim_thread.join()

    def run_user_view(self):
        # root = tk.Tk()
        # app = UserView(presenter, root)
        self.root.wm_title("Egypt Simulation")
        self.root.geometry("250x290")
        self.root.style = ttk.Style()
        self.root.style.theme_use("clam")
        self.root.mainloop()

    def statistics(self):
        """Convert and return household list as a pandas dataframe."""
        df = pd.DataFrame(columns=self.columns)
        for household in self.households:
            row = household.statistics()
            df = df.append(row, ignore_index=True)
        return df

    def river_map(self):
        """Return river_map numpy array attribute of environment object."""
        return self.environment.river_map

    def fertility_map(self):
        """Return fertility_map numpy array attribute of environment object."""
        return self.environment.fertility_map

    def update(self):
        """Tell frame view to save the current state of the simulation as a frame."""
        self.frame_view.save_frame()
        self.progress_var.set(self.generation + 1)
