from .isystem import ISystem
import numpy as np
from logic_simulation import Timer, ISimulate


DTYPE = np.float32



class Gain(ISystem):
    def __init__(self, timer:Timer, gain=1., ):
        self.__gain = gain
        self.__timer = timer

    @property
    def timer(self):
        return self.__timer

    @property
    def interval(self):
        return self.__timer.interval

    @property
    def gain(self):
        return self.__gain

    @gain.setter
    def gain(self, new_gain):
        self.__gain = new_gain

    def run_epoch(self, input_data, dtype=DTYPE):
        return dtype(self.__gain * input_data)
