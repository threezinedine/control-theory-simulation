from .isystem import ISystem
from logic_simulation import Timer
import numpy as np


DTYPE = np.float32


class Parallel(ISystem):
    def __init__(self, timer:Timer, sys=[]):
        self.__sys = sys
        self.__timer = timer

    @property
    def timer(self):
        return self.__timer

    @property
    def interval(self):
        return self.__timer.interval

    def run_epoch(self, input_data, dtype=DTYPE):
        result = 0
        for sys in self.__sys:
            result += sys.run_epoch(input_data, dtype=dtype)

        return dtype(result)
