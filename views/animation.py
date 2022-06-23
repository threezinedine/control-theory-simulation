import matplotlib.pyplot as plt
from decimal import Decimal


STEP = 0.01


def find_max_len(arr):
    max_len = Decimal('-inf')

    for ele in arr:
        if max_len < len(ele):
            max_len = len(ele)

    return max_len



class Animation:
    def __init__(self, lines=[], xlim=(0, 5), ylim=(-0.5, 1.5)):
        self.lines = lines
        self.xlim = xlim
        self.ylim = ylim

    def __len__(self):
        return find_max_len(self.lines)

    def set_up(self, ax):
        ax.set_xlim(self.xlim)
        ax.set_ylim(self.ylim)

    @property
    def must_clear(self):
        for line in self.lines:
            if line.must_clear:
                return True 
        
        return False

    def draw_step(self, ax, index):
        if self.must_clear:
            ax.clear()
            self.set_up(ax)

        for line in self.lines:
            line.draw(ax, index)

    def draw(self, ax, step=0.01):
        self.set_up(ax)
        for i in range(len(self)):
            self.draw_step(ax, i)
            plt.pause(step)


class AniParallel:
    def __init__(self, ani=[], ax=[], fig=None):
        self.anis = ani
        self.axes = ax
        self.fig = fig

    def __len__(self):
        return find_max_len(self.anis)

    def draw(self, step=0.01, xlim=(0, 5), ylim=(-0.5, 1.5)):
        for ani, ax in zip(self.anis, self.axes):
            ani.set_up(ax)

        for i in range(len(self)):
            for ani, ax in zip(self.anis, self.axes):
                ani.draw_step(ax, i)

            plt.pause(step)
