from .isignal import ISignal
import numpy as np


class Impulse(ISignal):
    def __init__(self, pulse_time=0.2):
        self.__pulse_time = np.float32(pulse_time)

    def generate(self, input_time:np.ndarray, dtype=np.float32):
        output = np.zeros_like(input_time, dtype=dtype)
        max_size = input_time.shape[-1]
        interval = input_time[1] - input_time[0]
        size = 0.5 / interval

        if input_time[0] > self.__pulse_time:
            return output


        for i, time in enumerate(input_time):
            if time == self.__pulse_time:
                output[i] = size
                if i < max_size - 1: 
                    output[i+1] = size
                break
            elif time > self.__pulse_time:
                output[i] = size
                output[i-1] = size
                break

        return output
