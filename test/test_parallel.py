import pytest
from logic_simulation import Timer
from system import Gain, Derivative, Integral, Parallel
import numpy as np


ROUND_DECIMALS = 3
DTYPE = np.float32
INTERVAL = 0.2
TIMER = Timer(interval=INTERVAL)


@pytest.mark.parametrize("gains, sys, input_data, expected", [
        ([2, 3], [Gain(TIMER), Gain(TIMER)], 4, DTYPE(20)),
        ([6, 3.5], [Gain(TIMER), Gain(TIMER)], 1, DTYPE(9.5)),
        ([6, 3.5, 3.1], [Gain(TIMER), Gain(TIMER), Gain(TIMER)], 2, DTYPE(25.2)),
    ])
def test_run_epoch_gain_gain(gains, sys, input_data, expected):
    for s, gain in zip(sys, gains): 
        s.gain = gain

    f_sys = Parallel(TIMER, sys=sys)
    
    result = f_sys.run_epoch(input_data)
    assert np.round(result, decimals=ROUND_DECIMALS) == np.round(expected, decimals=ROUND_DECIMALS)
