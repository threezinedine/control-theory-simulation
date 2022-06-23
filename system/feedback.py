from .isystem import ISystem
import numpy as np
from logic_simulation import Timer


DTYPE = np.float32


class Feedback(ISystem):
    def __init__(self, timer:Timer, input_sys:ISystem, feedback_gain=1):
        self.__timer = timer  
        self.__input_sys = input_sys
        self.__pre_out = 0
        self.__feedback_gain = feedback_gain
        self.__errors = []

    @property
    def timer(self):
        return self.__timer

    @property
    def interval(self):
        return self.__timer.interval

    @property
    def feedback_gain(self):
        return self.__feedback_gain

    @feedback_gain.setter
    def feedback_gain(self, new_gain):
        self.__feedback_gain = new_gain

    @property
    def pre_out(self):
        return self.__pre_out

    @pre_out.setter
    def pre_out(self, new_pre):
        self.__pre_out = new_pre

    def run_epoch(self, input_data, dtype=DTYPE):
        act_input = input_data - self.__feedback_gain * self.__pre_out
        self.__errors.append(act_input)
        self.__pre_out = self.__input_sys.run_epoch(act_input)

        return dtype(self.__pre_out)

    @property
    def errors(self):
        return np.array(self.__errors)
