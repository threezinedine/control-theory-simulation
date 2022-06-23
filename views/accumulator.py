from .ianimation import IAnmiation
import numpy as np


class Accumulator(IAnmiation):
    def __init__(self, input_x, input_y):
        self.input_x = input_x
        self.input_y = input_y

    def __len__(self):
        return self.input_x.shape[0]

    @property
    def must_clear(self):
        return False

    def get(self, index:int):
        if index < len(self):
            return self.input_x[:index], self.input_y[:index]
        else:
            return self.input_x, self.input_y



class OnTime(IAnmiation):
    def __init__(self, input_x, input_y, **kwargs):
        self.input_x = input_x
        self.input_y = input_y
        self._kwargs = kwargs

    def __len__(self):
        return self.input_x.shape[0]

    @property
    def must_clear(self):
        return True

    def get(self, index:int):
        if index < len(self):
            output_y = np.ones_like(self.input_x, dtype=np.float32) * self.input_y[index]
        else:
            output_y = np.ones_like(self.input_x, dtype=np.float32) * self.input_y[len(self) - 1]

        return self.input_x, output_y

    def draw(self, ax, index:int):
        IAnmiation.draw(self, ax, index, **self._kwargs)
