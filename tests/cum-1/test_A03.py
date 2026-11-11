
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from A03 import threshold


def test_threshold():
    image = np.array([[0, 50, 127, 128, 255]])
    expected = np.array([[0, 0, 0, 1, 1]])

    np.testing.assert_array_equal(
        threshold(image, 127), expected
    )


def test_threshold_255():
    image = np.array([[100, 200]])
    expected = np.array([[0, 255]])

    np.testing.assert_array_equal(
        threshold(image, 127, 255), expected
    )


def test_threshold_zero():
    image = np.array([[0, 1, 255]])

    np.testing.assert_array_equal(
        threshold(image, 0),
        [[0, 1, 1]]
    )


def test_invalid_threshold():
    with pytest.raises(ValueError):
        threshold([[100]], -1)


def test_invalid_pixel():
    with pytest.raises(ValueError):
        threshold([[300]], 127)
