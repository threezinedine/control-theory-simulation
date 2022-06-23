from .isystem import ISystem
from logic_simulation import Timer
import numpy as np


DTYPE = np.float32


class Integral(ISystem):
    def __init__(self, timer:Timer):
        self.__timer = timer
        self.__sum = 0
        self.__pre = 0

    @property
    def timer(self):
        return self.__timer

    @property
    def interval(self):
        return self.__timer.interval

    @property
    def pre(self):
        return self.__pre

    @pre.setter
    def pre(self, new_pre):
        self.__pre = new_pre

    @property
    def sum(self):
        return self.__sum

    @sum.setter
    def sum(self, new_sum):
        self.__sum = new_sum

    def run_epoch(self, input_data, dtype=DTYPE):
        self.__sum += (self.__pre + input_data) / 2 * self.interval
        self.__pre = input_data
        return dtype(self.__sum)
