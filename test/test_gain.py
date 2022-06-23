import pytest
from logic_simulation import Timer
from system import Gain
import numpy as np


ROUND_DECIMALS = 3
DTYPE = np.float32


@pytest.mark.parametrize("gain, input_data, expected", [
        (1, 5, DTYPE(5)),
        (-2, 3, DTYPE(-6))
    ])
def test_run_epoch(gain, input_data, expected):
    timer = Timer()
    sys = Gain(timer, gain=gain)

    result = sys.run_epoch(input_data)

    assert result == expected


@pytest.mark.parametrize("input_arr, expected, gain", [
        (np.array([0, 0.2, 0.4, 0.6, 0.8], dtype=DTYPE), np.array([0., 0.04, 0.08, 0.12, 0.16], dtype=DTYPE), 0.2),
        (np.array([0, 1, 2, 2], dtype=DTYPE), np.array([0., 0.5, 1, 1], dtype=DTYPE), 0.5)
    ])
def test_run(input_arr, expected, gain):
    timer = Timer()
    sys = Gain(gain=gain, timer=timer)

    result = sys.run(input_arr, dtype=DTYPE)

    assert np.equal(np.round(result, decimals=ROUND_DECIMALS), np.round(expected, decimals=ROUND_DECIMALS)).all()
