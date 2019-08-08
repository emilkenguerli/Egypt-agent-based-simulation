import math
from threading import Thread

import matplotlib.cm as mcm
import matplotlib.colors as mcolors
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np


class UserInterface(Thread):
    """ """


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
        fertility_map = self.presenter.fertility_map()
        river_img = self.river_img(river_map)
        fertility_img = self.fertility_img(fertility_map)
        display = fertility_img + river_img

        plt.figure(num='Egypt Simulator')
        self.plot_households()
        plt.imshow(display)
        plt.show()


    def plot_households(self):
        statistics = self.presenter.statistics()
        x_pos, y_pos = statistics['x_pos'], statistics['y_pos']
        num_workers = statistics['num_workers']
        grain = statistics['grain']
        knowledge_ratio = statistics['knowledge_ratio']
        competency = statistics['competency']
        ambition = statistics['ambition']

        knowledge_radii = knowledge_ratio*num_workers
        area = math.pi*(knowledge_radii**2)

        cnorm = mcolors.Normalize(vmin=0, vmax=1)
        scalar_map = mcm.ScalarMappable(norm=cnorm, cmap=plt.get_cmap('plasma'))
        competency_to_ambition = ambition/(ambition+competency)
        rgba = scalar_map.to_rgba(competency_to_ambition)

        grain_per_worker = grain/num_workers
        gpw_min, gpw_max = grain_per_worker.min(), grain_per_worker.max()
        alpha = np.interp(grain_per_worker, (gpw_min, gpw_max), (0.2, 0.8))
        rgba[:,-1] = alpha

        plt.scatter(x_pos, y_pos, s=area, color=rgba)


    def river_img(self, river_map):
        river_list = list(river_map)
        make_blue = lambda px: self.__BLUE if px == 1.0 else self.__BLACK
        # Assumes river pixels in river map have a value of 1.0.
        river_list = [list(map(make_blue, row)) for row in river_list]
        return np.array(river_list)


    def fertility_img(self, fertility_map):
        invert = np.ones(fertility_map.shape) - fertility_map
        colour_invert = 255*invert
        fertility_list = list(colour_invert)
        _, g, _ = self.__GREEN
        make_green = lambda px: (int(px), g, int(px)) if px != 255 else self.__WHITE
        fertility_list = [list(map(make_green, row)) for row in fertility_list]
        # The above code is very specific to how shades of green scale (in rgb colour format).
        return np.array(fertility_list)
