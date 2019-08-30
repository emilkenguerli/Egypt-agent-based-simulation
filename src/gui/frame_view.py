import math

import pandas as pd
from matplotlib.animation import FuncAnimation
from matplotlib.animation import ArtistAnimation
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.cm as mcm
import matplotlib.colors as mcolors
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np


class FrameView():
    """Act upon data from the presenter and save data in the relevant format."""

    def __init__(self, presenter):
        """Initialise FrameView attributes upon object instantiation.

        Keyword arguments:
        presenter           -- presenter object for data retrieval

        The presenter has the FrameView as an attribute and the FrameView has the presenter
        as an attribute. This is to facilitate the flow of information between
        these two layers.
        """
        self._FRAME_PATH = '../../resources/frames/'
        self._RIVER_BLUE = (102, 178, 255)
        self._GREEN = (0, 255, 0)
        self._WHITE = (255, 255, 255)
        self._BLACK = (0, 0, 0)
        self.presenter = presenter
        self.pop_df = pd.DataFrame(columns=['generation', 'population'])
        self.gini_df = pd.DataFrame(columns=['generation', 'gini-coefficient'])

    def save_frame(self):
        """Save household and landscape information as a frame.

        The relevant information is plotted as a matplotlib figure which is then
        saved as a .png file under the resources/frames folder.
        """
        statistics = self.presenter.statistics()
        river_map = self.presenter.river_map()
        fertility_map = self.presenter.fertility_map()
        river_img = self.river_img(river_map)
        fertility_img = self.fertility_img(fertility_map)
        display = fertility_img + river_img
        change_arrid = lambda x: x if tuple(x) != self._BLACK else self._WHITE
        display = np.apply_along_axis(change_arrid, axis=2, arr=display)

        fig = plt.figure()
        grid = plt.GridSpec(2, 2, wspace=0.3, hspace=0.5)

        x_pos, y_pos = self.get_pos(statistics)
        area = self.get_area(statistics)
        rgba = self.get_rgba(statistics)
        edges = self.get_edges(statistics, rgba)
        sim_axis = plt.subplot(grid[0:, 0])
        sim_axis.set_title('Year {0}'.format(self.presenter.get_generation()))
        sim_axis.scatter(x_pos, y_pos, s=area, color=rgba, edgecolors=edges)
        sim_axis.imshow(display)

        self.record_population(statistics)
        graph_1_axis = plt.subplot(grid[0, 1])
        graph_1_axis.set_title('Total Population')
        graph_1_axis.set_xlim([0, self.presenter.get_num_generations()])
        graph_1_axis.plot(self.pop_df['generation'], self.pop_df['population'])

        self.record_gini(statistics)
        graph_2_axis = plt.subplot(grid[1, 1])
        graph_2_axis.set_title('Gini-coefficient')
        graph_2_axis.set_xlim([0, self.presenter.get_num_generations()])
        graph_2_axis.set_ylim([0, 1])
        graph_2_axis.plot(self.gini_df['generation'], self.gini_df['gini-coefficient'], color=(1,0,0))

        path = self._FRAME_PATH + 'yr_{0}'.format(self.presenter.get_generation())
        plt.savefig(path)
        plt.close('all')

    def river_img(self, river_map):
        """Convert river_map into river_img and return as numpy array.

        Changing grayscale format to rgb format. River pixels will be mapped to
        blue otherwise black.
        """
        river_list = list(river_map)
        make_blue = lambda px: self._RIVER_BLUE if px == 1.0 else self._BLACK
        river_list = [list(map(make_blue, row)) for row in river_list]
        return np.array(river_list)

    def fertility_img(self, fertility_map):
        """Convert fertility_map into fertility_img and return as numpy array.

        Changing grayscale format to rgb format. Fertility pixels will be mapped
        to a shade of green otherwise white.
        """
        invert = np.ones(fertility_map.shape) - fertility_map
        colour_invert = 255*invert
        fertility_list = list(colour_invert)
        _, g, _ = self._GREEN
        make_green = lambda px: (int(px), g, int(px)) if px != 255 else self._BLACK
        fertility_list = [list(map(make_green, row)) for row in fertility_list]
        return np.array(fertility_list)

    def get_pos(self, statistics):
        """Return position tuple from household statistics."""
        x_pos, y_pos = statistics['x_pos'], statistics['y_pos']
        return (x_pos, y_pos)

    def get_area(self, statistics):
        """Return area of the marker to be plotted on the scatter figure."""
        knowledge_radius = statistics['knowledge_radius']
        return knowledge_radius**2

    def get_rgba(self, statistics):
        """Return numpy array rgba pixels values for all the household.

        Color (rgb channel)         -- determined by propensity to ambition or competency
        Opaqueness (alpha channel)  -- determined by grain per worker
        """
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
        alpha = np.interp(grain_per_worker, (gpw_min, gpw_max), (0.2, 1.0))
        rgba[:,-1] = alpha
        return rgba

    def get_edges(self, statistics, rgba):
        interaction = statistics['interaction']
        def to_edges(action, tuple):
            if action < 0:
                return (1, 0, 0)
            elif action > 0:
                return (0, 0, 1)
            else:
                return tuple
        return [to_edges(action, tuple) for action, tuple in zip(interaction, rgba)]

    def record_population(self, statistics):
        generation = self.presenter.get_generation()
        population = statistics['num_workers'].sum()
        row = {'generation':generation, 'population': population}
        self.pop_df = self.pop_df.append(row, ignore_index=True)

    def record_gini(self, statistics):
        generation = self.presenter.get_generation()
        total_grain = statistics['grain'].sum()
        grain = np.sort(statistics['grain'])
        wealth_prop = grain/total_grain
        num_households = len(statistics)
        pop_prop = np.ones(num_households)/num_households
        richer_prop = np.linspace(num_households - 1, 0, num=num_households)/num_households
        score = wealth_prop * (pop_prop + 2 * richer_prop)
        gini = 1 - score.sum()
        row = {'generation':generation, 'gini-coefficient':gini}
        self.gini_df = self.gini_df.append(row, ignore_index=True)
