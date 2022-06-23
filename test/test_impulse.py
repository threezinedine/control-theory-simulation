import pytest
from signals import Impulse
import numpy as np


@pytest.mark.parametrize("input_time, impulse_time, expetected", [
        (np.array([0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2], dtype=np.float32), 
            0.5, np.array([0., 0., 2.5, 2.5, 0., 0., 0.], dtype=np.float32)),
        (np.array([0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2], dtype=np.float32), 
            0.4, np.array([0., 0., 2.5, 2.5, 0., 0., 0.], dtype=np.float32)),
        (np.array([0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2], dtype=np.float32), 
            0.6, np.array([0., 0., 0.0, 2.5, 2.5, 0., 0.], dtype=np.float32)),
        (np.array([0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2], dtype=np.float32), 
            -1, np.array([0., 0., 0.0, 0., 0., 0., 0.], dtype=np.float32)),
        (np.array([0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2], dtype=np.float32), 
            1.2, np.array([0., 0., 0.0, 0., 0., 0., 2.5], dtype=np.float32))
    ])
def test_generate(input_time, impulse_time, expetected):
    signal =  Impulse(impulse_time)

    output = signal.generate(input_time)

    assert np.equal(output, expetected).all()
