from abc import ABC, abstractmethod, abstractproperty


class IAnmiation(ABC):
    @abstractmethod
    def get(self, index: int):
        pass

    @abstractmethod
    def __len__(self):
        pass

    @abstractproperty
    def must_clear(self):
        pass

    def draw(self, ax, index:int, **kwargs):
        x, y = self.get(index)
        ax.plot(x, y, **self.kwargs)
        
