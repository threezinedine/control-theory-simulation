from logic_simulation import Timer
from system import Feedback, ISystem, Integral, Gain, Serial, Parallel
from signals import Step, Impulse, ISignal
import warnings
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from views import Animation, OnTime, Accumulator, AniParallel, IAnmiation
from copy import deepcopy


DTYPE = np.float32
KP = 45
KI = 200
FONT_SIZE = 8
OUT_RATE = .3 
XLIM = (0, 3)
YLIM = (-.5, 5)


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
    signal = MySignal()
    fig, ax = plt.subplots(3, 2)

    # p system 
    p_term = Gain(timer, gain=KP)
    p_sys = Parallel(timer, sys=[p_term, Gain(timer, gain=KP)])
    p_cl_sys = Feedback(timer, input_sys=Serial(timer, sys=[p_sys, deepcopy(tank)]))
    time_arr, output = p_cl_sys.simulate(signal)
    ani_p_acc = Accumulator(time_arr, output)
    ani_p = Animation([ani_p_acc], xlim=XLIM, ylim=YLIM) 
    ani_p_errors_acc = Accumulator(time_arr, p_cl_sys.errors)
    ani_p_errors = Animation([ani_p_errors_acc], xlim=XLIM, ylim=YLIM)

    tank_ani_acc_p = TankLevelAnimatin(time_arr, output)
    expected_acc = OnTime(time_arr, signal.generate(time_arr), color='red', label="expected level")
    tank_ani_p = Animation([tank_ani_acc_p, expected_acc], xlim=XLIM, ylim=YLIM)


    # pi controller
    pi_term = Serial(timer, sys=[Gain(timer, gain=KI), Integral(timer)])
    pi_sys = Parallel(timer, sys=[pi_term, Gain(timer, gain=KP)])

    pi_cl_sys = Feedback(timer, input_sys=Serial(timer, sys=[pi_sys, deepcopy(tank)]))
    time_arr, output = pi_cl_sys.simulate(signal)
    ani_pi_acc = Accumulator(time_arr, output)
    ani_pi = Animation([ani_p_acc], xlim=XLIM, ylim=YLIM)

    ani_pi_errors_acc = Accumulator(time_arr, pi_cl_sys.errors)
    ani_pi_errors = Animation([ani_pi_errors_acc], xlim=XLIM, ylim=YLIM)

    tank_ani_acc_pi = TankLevelAnimatin(time_arr, output)
    tank_ani_pi = Animation([tank_ani_acc_pi, expected_acc], xlim=XLIM, ylim=YLIM)

    ax[0, 0].set_title("Tank level with p controller")
    ax[0, 1].set_title("Tank level with pi controller")
    ax[0, 0].set_ylabel("Current level")
    ax[1, 0].set_ylabel("Error")
    ax[2, 0].set_ylabel("Tank simulation")

    plt.legend(loc="best")
    wrapper = AniParallel([ani_p, ani_p_errors, ani_pi, ani_pi_errors, tank_ani_p, tank_ani_pi], 
            [ax[0, 0], ax[1, 0], ax[0, 1], ax[1, 1], ax[2, 0], ax[2, 1]], fig=fig)
    wrapper.draw(step=0.04)

    plt.plot()
    plt.show()
