
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from B05 import min_filter


def test_min_center():
    image = [
        [100, 102, 101],
        [99, 255, 103],
        [100, 98, 102]
    ]

    assert min_filter(image)[1, 1] == 98


def test_remove_salt_noise():
    image = np.full((5, 5), 100)
    image[2, 2] = 255

    assert min_filter(image)[2, 2] == 100


def test_uniform_image_center():
    image = np.full((5, 5), 90)

    assert min_filter(image)[2, 2] == 90


def test_zero_padding():
    np.testing.assert_array_equal(
        min_filter([[100]]), [[0]]
    )


def test_kernel_5():
    image = np.full((7, 7), 120)
    image[2, 2] = 40

    assert min_filter(image, 5)[3, 3] == 40


def test_output_shape():
    image = np.full((4, 6), 100)

    assert min_filter(image).shape == (4, 6)


def test_invalid_kernel():
    with pytest.raises(ValueError):
        min_filter([[100]], 4)


def test_invalid_pixel():
    with pytest.raises(ValueError):
        min_filter([[300]])


def test_invalid_dimension():
    with pytest.raises(ValueError):
        min_filter([10, 20, 30])


def test_empty_image():
    with pytest.raises(ValueError):
        min_filter(np.empty((0, 0)))
