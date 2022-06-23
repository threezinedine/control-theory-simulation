from abc import ABC, abstractmethod, abstractproperty
from signals import ISignal
import numpy as np


DTYPE = np.float32


class ISystem(ABC):
    @abstractproperty
    def timer(self):
        pass

    @abstractproperty
    def interval(self):
        pass

    @abstractmethod
    def run_epoch(self, input_data):
        pass

    def run(self, input_array, dtype=DTYPE):
        result = np.zeros_like(input_array, dtype=DTYPE) 
        for i, data_point in enumerate(input_array):
            result[i] = self.run_epoch(data_point, dtype=dtype)

        return result

    def simulate(self, input_signal:ISignal, dtype=DTYPE):
        time_arr = self.timer.get_time()
        input_arr = input_signal.generate(time_arr, dtype=dtype)
        output = self.run(input_arr, dtype=dtype)
        return time_arr, output
