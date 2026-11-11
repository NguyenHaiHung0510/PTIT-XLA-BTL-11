
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from A02 import adjust_brightness


def test_increase_brightness():
    image = np.array([[0, 50, 100, 200, 255]])
    expected = np.array([[0, 75, 150, 255, 255]])

    np.testing.assert_array_equal(
        adjust_brightness(image, 1.5), expected
    )


def test_decrease_brightness():
    image = np.array([[0, 50, 100, 200, 255]])
    expected = np.array([[0, 25, 50, 100, 128]])

    np.testing.assert_array_equal(
        adjust_brightness(image, 0.5), expected
    )


def test_identity():
    image = np.array([[10, 100, 255]])

    np.testing.assert_array_equal(
        adjust_brightness(image, 1.0), image
    )


def test_invalid_coefficient():
    with pytest.raises(ValueError):
        adjust_brightness([[100]], -1)


def test_invalid_pixel():
    with pytest.raises(ValueError):
        adjust_brightness([[300]], 1.5)
