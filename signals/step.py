from .isignal import ISignal
import numpy as np


class Step(ISignal):
    def __init__(self, step_time=0, final_val=1):
        self.__step_time = step_time
        self.__final_val = final_val

    def generate(self, input_time:np.ndarray, dtype=np.float32):
        output = np.zeros_like(input_time, dtype=dtype)

        for i, time in enumerate(input_time):
            if time >= self.__step_time:
                output[i] = self.__final_val


        return output
