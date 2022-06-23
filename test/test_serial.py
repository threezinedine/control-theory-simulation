import pytest
from logic_simulation import Timer
from system import Gain, Derivative, Integral, Serial
import numpy as np


ROUND_DECIMALS = 3
DTYPE = np.float32
INTERVAL = 0.2
TIMER = Timer(interval=INTERVAL)


@pytest.mark.parametrize("gain, pre_data, input_data, input_sys, expected", [
        (1, 4, 5, [Derivative(TIMER), Gain(TIMER)], DTYPE(5)),
        (2, 4, 5, [Derivative(TIMER), Gain(TIMER)], DTYPE(10)),
        (2, 4, 5, [Gain(TIMER), Derivative(TIMER)], DTYPE(30)), 
        (2, 4, 5, [Integral(TIMER), Gain(TIMER)], DTYPE(1.8)), 
        (1, 4, 5, [Integral(TIMER), Gain(TIMER)], DTYPE(0.9)),
        (1, 4, 5, [Integral(TIMER), Gain(TIMER)], DTYPE(0.9)), 
    ])
def test_run_epoch(gain, pre_data, input_data, input_sys, expected):
    com_sys = []

    for s in input_sys:
        if isinstance(s, Gain):
            s.gain = gain
        elif isinstance(s, Derivative):
            s.run_epoch(pre_data)
        elif isinstance(s, Integral):
            s.pre = pre_data

        com_sys.append(s)
    sys = Serial(TIMER, sys=com_sys)

    result = sys.run_epoch(input_data)
    assert result == expected


@pytest.mark.parametrize("gain, input_arr, input_sys, expected", [
        (1, np.array([0, 0.1, 0.2, 0.3]), [Derivative(TIMER), Gain(TIMER)], np.array([0, 0.5, 0.5, 0.5], dtype=DTYPE)),
        (2, np.array([0, 0.1, 0.2, 0.3]), [Derivative(TIMER), Gain(TIMER)], np.array([0, 1., 1., 1.], dtype=DTYPE)),
        (1, np.array([0, 0.1, 0.2, 0.3]), [Integral(TIMER), Gain(TIMER)], np.array([0, 0.01, 0.04, 0.09], dtype=DTYPE)),
    ])
def test_run(gain, input_arr, input_sys, expected):
    com_sys = []

    for s in input_sys:
        if isinstance(s, Gain):
            s.gain = gain

        com_sys.append(s)
    sys = Serial(TIMER, sys=com_sys)

    result = sys.run(input_arr, dtype=DTYPE)

    assert np.equal(np.round(result, decimals=ROUND_DECIMALS), np.round(expected, decimals=ROUND_DECIMALS)).all()
