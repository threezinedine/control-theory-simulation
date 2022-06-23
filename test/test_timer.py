import pytest
from logic_simulation import Timer
import os
import numpy as np


@pytest.mark.parametrize("start_time, end_time, interval, expected", 
            [(0, 1, 0.2, np.array([0, 0.2, 0.4, 0.6, 0.8], dtype=np.float32)),
             (-1, 3, 0.5, np.array([0, 0.5, 1., 1.5, 2., 2.5], dtype=np.float32)),
             (3, 2, 0.5, np.array([0., 0.5, 1., 1.5], dtype=np.float32)),
             (4, 7, 1, np.array([4, 5, 6], dtype=np.float32))]
        )
def test_get_time(start_time, end_time, interval, expected):
    timer = Timer() 
    timer.end = end_time
    timer.start = start_time
    timer.interval = interval

    result = timer.get_time()

    print(result, expected)
    assert np.equal(result, expected).all()
