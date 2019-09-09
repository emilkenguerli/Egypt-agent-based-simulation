import tkinter as tk
from tkinter import ttk
import time
import yaml
from ruamel.yaml import YAML

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
        self.buttons = []

        with open("../var_config.yml") as f:
            self.var_config = yaml.load(f)

        # Assigns default values
        self.var_config['num_households'] = 15
        self.var_config['households']['num_workers'] = 15
        self.var_config['households']['grain'] = 3000
        self.var_config['households']['worker_capability'] = 1000
        self.var_config['households']['min_competency'] = 0.2
        self.var_config['households']['min_ambition'] = 0.2

        with open("../var_config.yml", "w") as f:
            YAML().dump(self.var_config, f)

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
        self.buttons.append(run_button)

        view_button = tk.Button(button_frame, text="View", command=self.click_view_button)
        view_button.config(width=15)
        view_button.pack(side=tk.RIGHT, padx=4, pady=(5, 20))
        self.buttons.append(view_button)

        config_button = tk.Button(button_frame, text="Config", command=self.click_config_button)
        config_button.config(width=15)
        config_button.pack(side=tk.TOP, padx=4, pady=(5, 20))
        self.buttons.append(config_button)

        self.progress_bar = ttk.Progressbar(self, variable=self.progress_var, orient="horizontal",
                                            length=200, mode="determinate")
        self.progress_bar["maximum"] = self.presenter.get_num_generations() - 1
        self.progress_bar.pack()

        self.start = time.time()

    def click_run_button(self):
        """Starts the simulation and continuously runs the next simulated year
           Enables the View button and disables the Config button.
        """
        self.buttons[1].config(state='normal')
        self.buttons[2].config(state='disabled')
        self.start = time.time()
        self.master.after(5, self.progress)

    def click_config_button(self):
        """Displays the different customizable household parameters set to default values

        There are 6 Labels accompanied by adjacent spinboxes that allows the user to 
        customise the household paramaters

        There is a button at the bottom to save the changes. Run button is disabled to prevent 
        simulation from being started before changes are saved.

        """
        self.buttons[0].config(state='disabled')
        self.window = tk.Toplevel(self.master)
        self.window.wm_title("Configuration")
        self.spinners = []

        var = tk.StringVar(self.master)
        var.set(str(self.var_config['num_households']))

        label1 = tk.Label(self.window, text = "Num of Households")
        label1.grid(row = 0)
        item_1 = tk.Spinbox(self.window, from_= 0, to = 100, width = 5, textvariable=var)
        item_1.grid(row = 0, column = 1)
        self.spinners.append(item_1)
        
        var2 = tk.StringVar(self.master)
        var2.set(str(self.var_config['households']['num_workers']))

        label2 = tk.Label(self.window, text = "Num of workers")
        label2.grid(row = 1)
        item_2 = tk.Spinbox(self.window, from_= 0, to = 100, width = 5, textvariable=var2)
        item_2.grid(row = 1, column = 1)
        self.spinners.append(item_2)
        
        var3 = tk.StringVar(self.master)
        var3.set(str(self.var_config['households']['grain']))

        label3 = tk.Label(self.window, text = "Grain")
        label3.grid(row = 2)
        item_3 = tk.Spinbox(self.window, from_= 0, to = 10000, width = 5, textvariable=var3)
        item_3.grid(row = 2, column = 1)
        self.spinners.append(item_3)

        var4 = tk.StringVar(self.master)
        var4.set(str(self.var_config['households']['worker_capability']))
        
        label4 = tk.Label(self.window, text = "Worker Capability")
        label4.grid(row = 3)
        item_4 = tk.Spinbox(self.window, from_= 0, to = 10000, width = 5, textvariable=var4)
        item_4.grid(row = 3, column = 1)
        self.spinners.append(item_4)
        
        var5 = tk.StringVar(self.master)
        var5.set(str(self.var_config['households']['min_competency']))

        label5 = tk.Label(self.window, text = "Min Competency")
        label5.grid(row = 4)
        item_5 = tk.Spinbox(self.window, format="%.2f", from_= 0.0, to = 1.0, increment = 0.1, width = 5, textvariable=var5)
        item_5.grid(row = 4, column = 1)
        self.spinners.append(item_5)

        var6 = tk.StringVar(self.master)
        var6.set(str(self.var_config['households']['min_ambition']))

        label6 = tk.Label(self.window, text = "Min Ambition")
        label6.grid(row = 5)
        item_6 = tk.Spinbox(self.window, format="%.2f", from_= 0.0, to = 1.0, increment = 0.1, width = 5, textvariable=var6)
        item_6.grid(row = 5, column = 1)
        self.spinners.append(item_6)
        
        ok_button = tk.Button(self.window, text="OK", command=self.click_ok_button)
        ok_button.config(width=15)
        ok_button.grid(row = 6)
        

    def click_ok_button(self):
        """ Saves the changes and updates these changes in the var_config.yml file. Enables
            the Run button.
        """
        self.var_config['num_households'] = int(self.spinners[0].get())
        self.var_config['households']['num_workers'] = int(self.spinners[1].get())
        self.var_config['households']['grain'] = int(self.spinners[2].get())
        self.var_config['households']['worker_capability'] = int(self.spinners[3].get())
        self.var_config['households']['min_competency'] = float(self.spinners[4].get())
        self.var_config['households']['min_ambition'] = float(self.spinners[5].get())

        with open("../var_config.yml", "w") as f:
            YAML().dump(self.var_config, f)

        self.window.destroy()
        self.buttons[0].config(state='normal')

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
        if gen == self.presenter.get_num_generations():
            end = time.time()
            print("Finished	in %.3f seconds" % (end - self.start))

    def next_year_frame(self, img, gen):
        """Continuously loads and presents frames to the pop-up window."""
        if gen < self.presenter.get_num_generations():
            load = Image.open(self.FRAME_DIR + "yr_{0}.png".format(gen))
            render = ImageTk.PhotoImage(load)
            img.configure(image=render)
            img.image = render
            gen += 1
            img.after(self.SEC_PER_FRAME, self.next_year_frame, img, gen)
