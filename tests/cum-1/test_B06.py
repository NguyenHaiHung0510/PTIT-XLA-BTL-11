
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from B06 import max_filter


def test_max_center():
    image = [
        [100, 102, 101],
        [99, 0, 103],
        [100, 98, 102]
    ]

    assert max_filter(image)[1, 1] == 103


def test_remove_pepper_noise():
    image = np.full((5, 5), 100)
    image[2, 2] = 0

    assert max_filter(image)[2, 2] == 100


def test_uniform_image():
    image = np.full((5, 5), 90)

    np.testing.assert_array_equal(
        max_filter(image)[1:4, 1:4],
        np.full((3, 3), 90)
    )


def test_zero_padding():
    np.testing.assert_array_equal(
        max_filter([[100]]), [[100]]
    )


def test_kernel_5():
    image = np.full((7, 7), 100)
    image[2, 2] = 200

    assert max_filter(image, 5)[3, 3] == 200


def test_output_shape():
    image = np.full((4, 6), 100)

    assert max_filter(image).shape == (4, 6)


def test_invalid_kernel():
    with pytest.raises(ValueError):
        max_filter([[100]], 4)


def test_invalid_pixel():
    with pytest.raises(ValueError):
        max_filter([[300]])


def test_invalid_dimension():
    with pytest.raises(ValueError):
        max_filter([10, 20, 30])


def test_empty_image():
    with pytest.raises(ValueError):
        max_filter(np.empty((0, 0)))
