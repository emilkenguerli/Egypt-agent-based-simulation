import math

import cv2
from matplotlib.animation import FuncAnimation
from matplotlib.animation import ArtistAnimation
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.cm as mcm
import matplotlib.colors as mcolors
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np


class View():

    def __init__(self, presenter):
        self.__FRAME_PATH = '../../resources/frames/'
        self.__WHITE = (255, 255, 255)
        self.__BLACK = (0, 0, 0)
        self.__BLUE = (102, 178, 255)
        self.__GREEN = (0, 255, 0)
        self.presenter = presenter
        self.frame_count = 0

    def save_frame(self):
        statistics = self.presenter.statistics()
        river_map = self.presenter.river_map()
        fertility_map = self.presenter.fertility_map()
        river_img = self.river_img(river_map)
        fertility_img = self.fertility_img(fertility_map)
        display = fertility_img + river_img

        fig = plt.figure()
        x_pos, y_pos = self.get_pos(statistics)
        area = self.get_area(statistics)
        rgba = self.get_rgba(statistics)
        plt.scatter(x_pos, y_pos, s=area, color=rgba)
        plt.imshow(display)
        path = self.__FRAME_PATH + 'frame_{0}'.format(self.frame_count)
        plt.savefig(path)
        self.frame_count += 1
        plt.close('all')
        # TODO: It may be worth exploring updating the current figure instead
        # of replotting for every frame.

    def get_pos(self, statistics):
        x_pos, y_pos = statistics['x_pos'], statistics['y_pos']
        return (x_pos, y_pos)

    def get_area(self, statistics):
        num_workers = statistics['num_workers']
        knowledge_ratio = statistics['knowledge_ratio']
        knowledge_radii = knowledge_ratio*num_workers
        return math.pi*(knowledge_radii**2)

    def get_rgba(self, statistics):
        num_workers = statistics['num_workers']
        grain = statistics['grain']
        competency = statistics['competency']
        ambition = statistics['ambition']
        cnorm = mcolors.Normalize(vmin=0, vmax=1)
        scalar_map = mcm.ScalarMappable(norm=cnorm, cmap=plt.get_cmap('plasma'))
        competency_to_ambition = ambition/(ambition+competency)
        rgba = scalar_map.to_rgba(competency_to_ambition)

        grain_per_worker = grain/num_workers
        gpw_min, gpw_max = grain_per_worker.min(), grain_per_worker.max()
        alpha = np.interp(grain_per_worker, (gpw_min, gpw_max), (0.2, 0.8))
        rgba[:,-1] = alpha
        return rgba

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
