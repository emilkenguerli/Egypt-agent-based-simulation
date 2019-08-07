from threading import Thread

import matplotlib.colors as mcolors
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np


class UserInterface(Thread):
    def __init__(self, presenter):
        Thread.__init__(self)
        self.__WHITE = (255, 255, 255)
        self.__BLACK = (0, 0, 0)
        self.__BLUE = (102, 178, 255)
        self.__GREEN = (0, 255, 0)
        self.presenter = presenter


    def run(self):
        statistics = self.presenter.statistics()
        river_map = self.presenter.river_map()
        flood_map = self.presenter.flood_map()
        river_img = self.river_img(river_map)
        flood_img = self.flood_img(flood_map)
        display = flood_img + river_img
        plt.imshow(display)
        plt.show()

    def river_img(self, river_map):
        river_list = list(river_map)
        make_blue = lambda px: self.__BLUE if px == 1.0 else self.__BLACK
        # Assumes river pixels in river map have a value of 1.0.
        river_list = [list(map(make_blue, row)) for row in river_list]
        return np.array(river_list)

    def flood_img(self, flood_map):
        invert = np.ones(flood_map.shape) - flood_map
        colour_invert = 255*invert
        flood_list = list(colour_invert)
        _, g, _ = self.__GREEN
        make_green = lambda px: (int(px), g, int(px)) if px != 255 else self.__WHITE
        flood_list = [list(map(make_green, row)) for row in flood_list]
        # The above code is very specific to how shades of green scale (in rgb colour format).
        return np.array(flood_list)
