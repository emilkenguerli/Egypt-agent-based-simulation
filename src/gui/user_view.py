from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

class Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.config(background="white")
        self.pack(fill=tk.BOTH, expand=True)

        load = Image.open("../../resources/pictures/iris.png")
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

        progress = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        progress.pack()


    def click_run_button(self):
        exit()

    def click_view_button(self):
        exit()

root = tk.Tk()
app = Window(root)
root.wm_title("Egypt Simulation")
root.geometry("250x290")
root.style = ttk.Style()
root.style.theme_use("clam")
root.mainloop()
