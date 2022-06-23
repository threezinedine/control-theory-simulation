from logic_simulation import Timer
from gif_concat import *
from system import Feedback, ISystem, Integral, Gain, Serial, Parallel
from signals import Step, Impulse, ISignal
import warnings
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from views import Animation, OnTime, Accumulator, AniParallel, IAnmiation


DTYPE = np.float32
KP = 45
KI = 200
FONT_SIZE = 8
OUT_RATE = .3 


class TankLevelAnimatin(IAnmiation):
    def __init__(self, input_time, data):
        self._input_time = input_time
        self._data = data

    def __len__(self):
        return self._input_time.shape[0]

    @property
    def must_clear(self):
        return True

    def get(self, index:int):
        return patches.Rectangle((0, 0), 5, self._data[index], linewidth=1)

    def draw(self, ax, index):
        ax.add_patch(self.get(index))


class Tank(ISystem):
    def __init__(self, timer:Timer, capacity=100, init=0):
        self.__current = init
        self.__capacity = capacity
        self.__timer = timer
        self.__sys = Integral(timer)
        self.__sys.sum = init

    @property
    def timer(self):
        return self.__timer

    @property
    def interval(self):
        return self.__timer.interval

    @property
    def capacity(self):
        return self.__capacity

    @property
    def current(self):
        return self.__current

    @current.setter
    def current(self, new_current):
        if (new_current > self.capacity):
            warnings.warn("The current value must be less than the capacity.") 

    @property
    def sys(self):
        return self.__sys

    def run_epoch(self, input_arr, dtype=DTYPE):
        output = self.__sys.run_epoch(input_arr, dtype=dtype) - OUT_RATE
        output = output if output > 0 else 0
        self.__sys.sum = output
        return output


class MySignal(ISignal):
    def generate(self, input_arr, dtype=DTYPE):
        result = np.zeros_like(input_arr, dtype=DTYPE)

        for i, input_data in enumerate(input_arr):
            if input_data < 1.5:
                result[i] = 3.
            else:
                result[i] = 1.

        return result


if __name__ == "__main__":
    timer = Timer(end_time=3., interval=0.01)
    tank = Tank(timer)
    tank2 = Tank(timer)
    tank3 = Tank(timer)
    signal = MySignal()
    fig = plt.figure()
    ax = plt.subplot(2, 2, 1)
    ax2 = plt.subplot(2, 2, 2)
    ax5 = plt.subplot(2, 2, 3)

#    op_sys = Serial(timer, sys=[Gain(timer, gain=23), tank])
    i_term = Serial(timer, sys=[Gain(timer, gain=KI), Integral(timer)])
    pid_sys = Parallel(timer, sys=[i_term, Gain(timer, gain=KP)])

    pid_cl_sys = Feedback(timer, input_sys=Serial(timer, sys=[pid_sys, tank]))
    time_arr, output = pid_cl_sys.simulate(signal)
    ani_p_acc = Accumulator(time_arr, output)
    ani_p = Animation([ani_p_acc], xlim=(0, 3), ylim=(-.5, 5))

    ani_p_errors_acc = Accumulator(time_arr, pid_cl_sys.errors)
    ani_p_errors = Animation([ani_p_errors_acc], xlim=(0, 3), ylim=(-.5, 5))


    tank_ani_acc = TankLevelAnimatin(time_arr, output)
    expected_acc = OnTime(time_arr, signal.generate(time_arr), color='red')
    tank_ani = Animation([tank_ani_acc, expected_acc], xlim=(0, 3), ylim=(-.5, 5))


    wrapper = AniParallel([ani_p, ani_p_errors, tank_ani], [ax, ax2, ax5], fig=fig)
    wrapper.draw(step=0.04)

    plt.plot()
