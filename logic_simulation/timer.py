import warnings
import numpy as np


class Timer:
    def __init__(self, start_time=0, end_time=1, interval=0.02):
        self.__start = start_time
        self.__end = end_time
        self.__interval = interval

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, new_start):
        if (new_start > self.__end):
            warnings.warn("The start time must be less than zero.")
        elif (new_start < 0):
            warnings.warn("The start time must be larger than zero.")
        else:
            self.__start = new_start

    @property
    def end(self):
        return self.__end

    @end.setter
    def end(self, new_end):
        if (new_end <= self.__start):
            warnings.warn(f"The end time must be larger than the start time ({self.__start})")
        else:
            self.__end = new_end

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, new_interval):
        self.__interval = new_interval

    def get_time(self, dtype=np.float32):
        return np.arange(self.__start, self.__end, self.__interval, dtype=dtype)
