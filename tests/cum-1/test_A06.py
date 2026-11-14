
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from A06 import contrast_stretch


def test_endpoints():
    np.testing.assert_array_equal(
        contrast_stretch([[0, 255]]),
        [[0, 255]]
    )


def test_control_points():
    np.testing.assert_array_equal(
        contrast_stretch([[80, 160]]),
        [[30, 220]]
    )


def test_first_segment():
    assert contrast_stretch([[40]])[0, 0] == 15


def test_middle_segment():
    assert contrast_stretch([[120]])[0, 0] == 125


def test_last_segment():
    assert contrast_stretch([[200]])[0, 0] == 235


def test_same_shape():
    image = np.array([[20, 50], [100, 200]])

    assert contrast_stretch(image).shape == image.shape


def test_invalid_points():
    with pytest.raises(ValueError):
        contrast_stretch([[100]], r1=160, r2=80)


def test_invalid_pixel():
    with pytest.raises(ValueError):
        contrast_stretch([[300]])


def test_invalid_dimension():
    with pytest.raises(ValueError):
        contrast_stretch([10, 20, 30])
