
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from B07 import midpoint_filter


def test_midpoint_center():
    image = [
        [100, 110, 120],
        [90, 150, 130],
        [80, 140, 160]
    ]

    assert midpoint_filter(image)[1, 1] == 120


def test_round_half_up():
    image = [
        [10, 10, 10],
        [10, 20, 11],
        [10, 10, 11]
    ]

    # (10 + 20) / 2 = 15
    assert midpoint_filter(image)[1, 1] == 15

    image[1][1] = 21
    # (10 + 21) / 2 = 15.5 -> 16
    assert midpoint_filter(image)[1, 1] == 16


def test_uniform_image_center():
    image = np.full((5, 5), 100)

    assert midpoint_filter(image)[2, 2] == 100


def test_zero_padding():
    # Min = 0, Max = 100 -> midpoint = 50
    np.testing.assert_array_equal(
        midpoint_filter([[100]]), [[50]]
    )


def test_kernel_5():
    image = np.full((7, 7), 100)
    image[2, 2] = 40
    image[4, 4] = 200

    # Min = 40, Max = 200 -> 120
    assert midpoint_filter(image, 5)[3, 3] == 120


def test_output_shape():
    image = np.full((4, 6), 100)

    assert midpoint_filter(image).shape == (4, 6)


def test_invalid_kernel():
    with pytest.raises(ValueError):
        midpoint_filter([[100]], 4)


def test_invalid_pixel():
    with pytest.raises(ValueError):
        midpoint_filter([[300]])


def test_invalid_dimension():
    with pytest.raises(ValueError):
        midpoint_filter([10, 20, 30])


def test_empty_image():
    with pytest.raises(ValueError):
        midpoint_filter(np.empty((0, 0)))
