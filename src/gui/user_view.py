from threading import Thread
import time
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

class UserView(tk.Frame):
    def __init__(self, presenter, progress_var, master=None):
        tk.Frame.__init__(self, master)
        self.PIC_DIR = "../../resources/pictures/"
        self.FRAME_DIR = "../../resources/frames/"
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

        self.progress_bar = ttk.Progressbar(self, variable=self.progress_var, orient="horizontal", length=200, mode="determinate")
        self.progress_bar["maximum"] = self.presenter.get_num_generations() - 1
        self.progress_bar.pack()

    def click_run_button(self):
        self.master.after(0, self.progress)

    def click_view_button(self):
        window = tk.Toplevel(self.master)
        window.wm_title("Egypt Simulation")
        load = Image.open(self.FRAME_DIR + "yr_0.png")
        render = ImageTk.PhotoImage(load)
        img = tk.Label(window, image=render, borderwidth=0)
        img.image = render
        img.pack()
        gen = 1
        img.after(1000, self.next_year_frame, img, gen)

    def progress(self):
        self.presenter.simulate_year()
        gen = self.presenter.get_generation()
        if gen < self.presenter.get_num_generations():
            self.progress_var.set(self.presenter.get_generation())
            self.master.after(0, self.progress)

    def next_year_frame(self, img, gen):
        if gen < self.presenter.get_num_generations():
            load = Image.open(self.FRAME_DIR + "yr_{0}.png".format(gen))
            render = ImageTk.PhotoImage(load)
            img.configure(image=render)
            img.image = render
            gen += 1
            img.after(1000, self.next_year_frame, img, gen)
            # TODO: change to frames per second constant
