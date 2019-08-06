from threading import Thread

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np


class UserInterface(Thread):
    def __init__(self, presenter):
        Thread.__init__(self)
        self.presenter = presenter


    def run(self):
        statistics = self.presenter.statistics()
        map = self.presenter.map()
        plt.imshow(map)
        plt.show()
        print(statistics)
        
