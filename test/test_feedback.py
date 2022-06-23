import pytest
from system import Feedback, Gain
import numpy as np
from logic_simulation import Timer


ROUND_DECIMALS = 3
DTYPE = np.float32
INTERVAL = 0.2
TIMER = Timer(interval=INTERVAL)


@pytest.mark.parametrize("pre, input_data, sys, gain, back_gain, expected", [
        (2, 3, Gain(TIMER), 1, 1, DTYPE(1)),  
        (4, 3, Gain(TIMER), 2, -1, DTYPE(14)),  
    ])
def test_run_epoch_gain(pre, input_data, sys, gain, back_gain, expected):
    sys.gain = gain
    cl_sys = Feedback(TIMER, sys, feedback_gain=back_gain)
    cl_sys.pre_out = pre

    result = cl_sys.run_epoch(input_data)

    assert np.round(expected, decimals=ROUND_DECIMALS) == np.round(result, decimals=ROUND_DECIMALS)
