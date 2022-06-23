from .isystem import ISystem
from logic_simulation import Timer, ISimulate
import numpy as np


DTYPE = np.float32


class Serial(ISystem):
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
        output = input_data
        for s in self.__sys:
            output = s.run_epoch(output, dtype=dtype)
        return dtype(output)
