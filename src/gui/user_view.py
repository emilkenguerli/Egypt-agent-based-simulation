from tkinter import ttk
import tkinter as tk

from PIL import Image, ImageTk

class UserView(tk.Frame):
    def __init__(self, presenter, progress_var, master=None):
        tk.Frame.__init__(self, master)
        self.presenter = presenter
        self.progress_var = progress_var
        self.master = master
        self.config(background="white")
        self.pack(fill=tk.BOTH, expand=True)

        load = Image.open("../../resources/pictures/iris.png")
        # TODO: change directory to constant attribute.
        load = load.resize((200, 200))
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
        self.progress_bar["maximum"] = self.presenter.get_num_generations()
        self.progress_bar.pack()

    def click_run_button(self):
        self.presenter.start_simulation()
        self.progress_var.set(self.presenter.get_num_generations())

    def click_view_button(self):
        window = tk.Toplevel(self.master)
