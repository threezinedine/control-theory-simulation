from abc import ABC, abstractmethod, abstractproperty
from signals import ISignal
import numpy as np


DTYPE = np.float32


class ISimulate(ABC):
    @abstractproperty
    def timer(self):
        pass

