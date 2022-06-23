import pytest
from logic_simulation import Timer
from system import Integral
import numpy as np


ROUND_DECIMALS = 3
DTYPE = np.float32


@pytest.mark.parametrize("pre_data, input_data, interval, expected", [
        (3, 5, 0.2, DTYPE(0.8)),
        (0, -2, 0.5, DTYPE(-0.5))
    ])
def test_run_epoch(pre_data, input_data, interval, expected):
    timer = Timer()
    timer.interval = interval
    sys = Integral(timer)
    sys.pre = pre_data

    result = sys.run_epoch(input_data)

    assert result == expected


@pytest.mark.parametrize("input_arr, expected, interval", [
        (np.array([0, 0.2, 0.4, 0.6, 0.8], dtype=DTYPE), np.array([0., 0.02, 0.08, 0.18, 0.32], dtype=DTYPE), 0.2),
        (np.array([0, 1, 2, 2], dtype=DTYPE), np.array([0., 0.25, 1, 2], dtype=DTYPE), 0.5)
    ])
def test_run(input_arr, expected, interval):
    timer = Timer()
    timer.interval = interval
    sys = Integral(timer) 
    sys.pre = 0

    result = sys.run(input_arr)

    assert np.equal(np.round(result, decimals=ROUND_DECIMALS), np.round(expected, decimals=ROUND_DECIMALS)).all()
