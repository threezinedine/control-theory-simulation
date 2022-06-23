from abc import ABC, abstractmethod, abstractproperty
import numpy as np


DTYPE = np.float32


class ISignal(ABC):
    @abstractmethod
    def generate(self, input_time:np.ndarray, dtype=DTYPE):
        pass
