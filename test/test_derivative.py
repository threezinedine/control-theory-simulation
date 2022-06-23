import pytest
from logic_simulation import Timer
from system import Derivative
import numpy as np


ROUND_DECIMALS = 3
DTYPE = np.float32


@pytest.mark.parametrize("pre_data, input_data, interval, expected", [
        (3, 5, 0.2, DTYPE(10)),
        (0, -2, 0.5, DTYPE(-4))
    ])
def test_run_epoch(pre_data, input_data, interval, expected):
    timer = Timer()
    timer.interval = interval
    sys = Derivative(timer)
    sys.run_epoch(pre_data)

    result = sys.run_epoch(input_data)

    assert result == expected


@pytest.mark.parametrize("input_arr, expected, interval", [
        (np.array([0, 0.2, 0.4, 0.6, 0.8], dtype=DTYPE), np.array([0., 1., 1., 1., 1], dtype=DTYPE), 0.2),
        (np.array([0, 1, 2, 2], dtype=DTYPE), np.array([0., 2., 2., 0.], dtype=DTYPE), 0.5)
    ])
def test_run(input_arr, expected, interval):
    timer = Timer()
    timer.interval = interval
    sys = Derivative(timer) 

    result = sys.run(input_arr)

    assert np.equal(np.round(result, decimals=ROUND_DECIMALS), np.round(expected, decimals=ROUND_DECIMALS)).all()
