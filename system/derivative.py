from .isystem import ISystem
from logic_simulation import Timer
import numpy as np


DTYPE = np.float32



class Derivative(ISystem):
    def __init__(self, timer:Timer):
        self.__pre = 0
        self.__timer = timer

    @property
    def interval(self):
        return self.__timer.interval

    @property
    def timer(self):
        return self.__timer

    @interval.setter
    def interval(self, interval):
        self.__interval = interval

    def run_epoch(self, input_data, dtype=DTYPE):
        result = (input_data - self.__pre) / self.interval
        self.__pre = input_data
        return dtype(result)
