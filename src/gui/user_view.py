import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

class UserView(tk.Frame):
    """Encapsulates all gui functionality."""

    def __init__(self, presenter, progress_var, master=None):
        """Initialises UserView upon object instantiation.

        An image, two buttons and a progress bar are rendered on the main window
        upon application execution.

        Args:
            presenter: Presenter singleton object.
            progress_var: tkinter.IntVar that the progress_bar widget monitors
                to update its progress.
            master: Root window of the application.
        """
        tk.Frame.__init__(self, master)
        self.PIC_DIR = "../../resources/pictures/"
        self.FRAME_DIR = "../../resources/frames/"
        self.SEC_PER_FRAME = 1000
        self.presenter = presenter
        self.progress_var = progress_var
        self.master = master
        self.config(background="white")
        self.pack(fill=tk.BOTH, expand=True)

        load = Image.open(self.PIC_DIR + "iris.png")
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image=render, borderwidth=0)
        img.image = render
        img.pack()

        button_frame = tk.Frame(self)
        button_frame.config(background="white")
        button_frame.pack()

        run_button = tk.Button(button_frame, text="Run", command=self.click_run_button)
        run_button.config(width=15)
        run_button.pack(side=tk.LEFT, padx=4, pady=(5, 20))

        view_button = tk.Button(button_frame, text="View", command=self.click_view_button)
        view_button.config(width=15)
        view_button.pack(side=tk.RIGHT, padx=4, pady=(5, 20))

        self.progress_bar = ttk.Progressbar(self, variable=self.progress_var, orient="horizontal",
                                            length=200, mode="determinate")
        self.progress_bar["maximum"] = self.presenter.get_num_generations() - 1
        self.progress_bar.pack()

    def click_run_button(self):
        """Starts the simulation and continuously runs the next simulated year."""
        self.master.after(5, self.progress)

    def click_view_button(self):
        """Displays the simulation frames in a pop-up window.

        The first frame is displayed in the pop-up window after which it is
        updated every SEC_PER_FRAME (as per the next_year_frame method).
        """
        window = tk.Toplevel(self.master)
        window.wm_title("Egypt Simulation")
        load = Image.open(self.FRAME_DIR + "yr_0.png")
        render = ImageTk.PhotoImage(load)
        img = tk.Label(window, image=render, borderwidth=0)
        img.image = render
        img.pack()
        gen = 1
        img.after(self.SEC_PER_FRAME, self.next_year_frame, img, gen)

    def progress(self):
        """Continuously simulates a year and updates the progress variable."""
        self.presenter.simulate_year()
        gen = self.presenter.get_generation()
        if gen < self.presenter.get_num_generations():
            self.progress_var.set(self.presenter.get_generation())
            self.master.after(5, self.progress)

    def next_year_frame(self, img, gen):
        """Continuously loads and presents frames to the pop-up window."""
        if gen < self.presenter.get_num_generations():
            load = Image.open(self.FRAME_DIR + "yr_{0}.png".format(gen))
            render = ImageTk.PhotoImage(load)
            img.configure(image=render)
            img.image = render
            gen += 1
            img.after(self.SEC_PER_FRAME, self.next_year_frame, img, gen)
