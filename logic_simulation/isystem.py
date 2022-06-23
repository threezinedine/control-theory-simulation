from abc import ABC, abstractmethod


class ISystem:
    @abstractmethod
    def run(self, input_arr):
        raise NotImplementedError("running function must be implementd")
