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
    def __init__(self, lines=[]):
        self.lines = lines

    def __len__(self):
        return find_max_len(self.lines)

    def set_up(self, ax , xlim=(0, 5), ylim=(-0.5, 1.5)):
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

    def draw_step(self, ax, index, xlim, ylim):
        ax.clear()
        self.set_up(ax, xlim, ylim)
        for line in self.lines:
            line.draw(ax, index)

    def draw(self, ax, step=0.01, xlim=(0, 5), ylim=(-0.5, 1.5)):
        self.set_up(ax, xlim, ylim)
        for i in range(len(self)):
            self.draw_step(ax, i, xlim, ylim)
            plt.pause(step)


class AniParallel:
    def __init__(self, ani=[], ax=[], fig=None):
        self.anis = ani
        self.axes = ax
        self.fig = fig
        self._index = 0

    def __len__(self):
        return find_max_len(self.anis)

    def draw(self, step=0.01, xlim=(0, 5), ylim=(-0.5, 1.5)):
        for ani, ax in zip(self.anis, self.axes):
            ani.set_up(ax, xlim, ylim)

        for i in range(len(self)):
            for ani, ax in zip(self.anis, self.axes):
                ani.draw_step(ax, i, xlim, ylim)

            self.fig.savefig(f"images/img_{self._index}.png", bbox_inches='tight', dpi=self.fig.dpi)
            self._index += 1
            plt.pause(step)
