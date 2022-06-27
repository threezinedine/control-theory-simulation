from logic_simulation import Timer
from system import Gain, ISystem, Derivative, Serial, Integral, Feedback, Parallel
from signals import ISignal, Step, Impulse
from views import Animation, AniParallel, Accumulator, OnTime, IAnmiation, OnOut
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from copy import deepcopy


DTYPE = np.float32
MASS = 0.1
KP = 2 
STEP = 1e-8
SPEED_UP = 500
Y_LIM = (-4, 9)
X_LIM = (0, 2)



class MagneticTrain(ISystem):
    def __init__(self, timer:Timer, init_pos, max_x=15):
        self._pos = init_pos
        self.__timer = timer
        self._max_x = max_x

        #define the system
        self._sys = Serial(timer, sys=[Gain(timer, gain=1./MASS), Integral(timer,), Integral(timer,)])

    @property
    def timer(self):
        return self.__timer

    @property
    def interval(self):
        return self.__timer.interval

    @property
    def max_x(self):
        return self._max_x

    def run_epoch(self, input_data, dtype=DTYPE):
#        self._pos = self._pos + self._sys.run_epoch(input_data, dtype=dtype)
#
#        self._pos = self._pos if self._pos < self.max_x else self.max_x
#
#        return self._pos
        return self._sys.run_epoch(input_data, dtype=dtype)

class TrainAnimation(IAnmiation):
    def __init__(self, time_arr, output, width=1, height=1):
        self.time_arr = time_arr
        self.output = output
        self.width = width
        self.height = height

    def __len__(self):
        return self.time_arr.shape[0]

    @property
    def must_clear(self):
        return True

    def get(self, index:int):
        return self.output[index] - self.height/2, 0

    def draw(self, ax, index:int, **kwargs):
        x, y = self.get(index)
        rect = Rectangle((x, y), self.width, self.height)
        ax.add_patch(rect)


if __name__ == "__main__":
    timer = Timer(end_time=2, interval=1e-4)
    train = MagneticTrain(timer, 0, 45)
    signal = Step(final_val=4)
    fig, ax = plt.subplots(3, 2)

    #system with p controller
    p_control = Gain(timer, gain=KP)
    p_train = Feedback(timer, input_sys=Serial(timer, sys=[p_control, deepcopy(train)]))

    time_arr, output = p_train.simulate(signal)
    p_train_ani = Accumulator(time_arr, output, color='red')
    p_train_animation = Animation(lines=[p_train_ani], ylim=Y_LIM, xlim=X_LIM)

    p_train_error_ani = Accumulator(time_arr, p_train.errors)

    p_train_error_animation = Animation(lines=[p_train_error_ani], ylim=Y_LIM, xlim=X_LIM)

    # sys ani with p
    sys_ani_p = TrainAnimation(time_arr, output)
    expected = OnOut(time_arr, signal.generate(time_arr), color='red')

    sys_ani_p = TrainAnimation(time_arr, output)
    sys_animation_p = Animation(lines=[sys_ani_p, expected], xlim=(0, 14), ylim=(-1, 4))

    # system with pd controller
    pd_control = Parallel(timer, sys=[Gain(timer, gain=KP), Derivative(timer)])
    pd_train = Feedback(timer, input_sys=Serial(timer, sys=[pd_control, deepcopy(train)]))

    time_arr, output = pd_train.simulate(signal)
    pd_train_ani = Accumulator(time_arr, output)
    pd_train_animation = Animation(lines=[pd_train_ani], ylim=Y_LIM, xlim=X_LIM)

    pd_train_error_ani = Accumulator(time_arr, pd_train.errors)
    pd_train_error_animation = Animation(lines=[pd_train_error_ani], ylim=Y_LIM, xlim=X_LIM)

    # system animation
    sys_ani_pd = TrainAnimation(time_arr, output)
    sys_animation_pd = Animation(lines=[sys_ani_pd, expected], xlim=(0, 6), ylim=(-1, 4))

    ax[0, 0].set_title("Train with p controller") 
    ax[0, 1].set_title("Train with pi controller") 
    ax[0, 0].set_ylabel("Current position") 
    ax[1, 0].set_ylabel("Errors") 

    wrapper = AniParallel(ani=[p_train_animation, p_train_error_animation, pd_train_animation, pd_train_error_animation, sys_animation_p, sys_animation_pd], 
            ax=[ax[0, 0], ax[1, 0], ax[0, 1], ax[1, 1], ax[2, 0], ax[2, 1]], fig=fig)
    wrapper.draw(step=STEP, speed_up=SPEED_UP)

    plt.show()
