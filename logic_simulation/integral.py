import numpy as np 
from .isystem import ISystem


class Integral(ISystem):
    def __init__(self, interval):
        self.__interval = interval

    def run(self, input_arr, dtype=np.float32):
        result = np.zeros_like(input_arr, dtype=dtype)
        
        for i in range(1, input_arr.shape[0]):
            result[i] = result[i-1] + (input_arr[i-1] + input_arr[i]) * self.__interval / 2

        return result
