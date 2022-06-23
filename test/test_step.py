import pytest
from signals import Step
import numpy as np


@pytest.mark.parametrize("step_time, final_val, input_time, expetected", [
        (1, 1, np.array([0., 0.2, 0.4, 0.8, 1.0, 1.2, 1.4], dtype=np.float32), 
            np.array([0., 0., 0., 0., 1., 1., 1.], dtype=np.float32)),

        (1, 2, np.array([0., 0.2, 0.4, 0.8, 1.0, 1.2, 1.4], dtype=np.float32), 
            np.array([0., 0., 0., 0., 2., 2., 2.], dtype=np.float32)),
        (0.5, 1, np.array([0., 0.2, 0.4, 0.8, 1.0, 1.2, 1.4], dtype=np.float32), 
            np.array([0., 0., 0., 1., 1., 1., 1.], dtype=np.float32))
    ])
def test_generate(step_time, final_val, input_time, expetected):
    signal = Step(step_time=step_time, final_val=final_val)
    
    output = signal.generate(input_time)

    assert np.equal(output, expetected).all()

