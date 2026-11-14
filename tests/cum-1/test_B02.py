
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from B02 import (
    weighted_filter,
    weighted_mean_filter,
    gaussian_filter,
    WEIGHTED_3X3,
    GAUSSIAN_5X5
)


def test_weighted_kernel_sum():
    assert np.isclose(WEIGHTED_3X3.sum(), 1)


def test_gaussian_kernel_sum():
    assert np.isclose(GAUSSIAN_5X5.sum(), 1)


def test_weighted_center():
    image = np.zeros((5, 5), dtype=int)
    image[2, 2] = 160

    # Trong so tam = 4/16, ket qua = 40
    assert weighted_mean_filter(image)[2, 2] == 40


def test_gaussian_center():
    image = np.zeros((7, 7), dtype=int)
    image[3, 3] = 159

    # Trong so tam = 15/159, ket qua = 15
    assert gaussian_filter(image)[3, 3] == 15


def test_uniform_center():
    image = np.full((7, 7), 100)

    assert weighted_mean_filter(image)[3, 3] == 100
    assert gaussian_filter(image)[3, 3] == 100


def test_zero_padding():
    image = np.array([[160]])

    # Cua so 3x3, chi co pixel tam
    assert weighted_mean_filter(image)[0, 0] == 40


def test_output_shape():
    image = np.full((8, 10), 100)

    assert gaussian_filter(image).shape == image.shape


def test_custom_kernel():
    image = np.array([[10, 20, 30]])

    # Kernel 1x1 giu nguyen anh
    result = weighted_filter(image, [[1]])

    np.testing.assert_array_equal(result, image)


def test_invalid_kernel():
    with pytest.raises(ValueError):
        weighted_filter([[100]], [[1, 1], [1, 1]])


def test_invalid_pixel():
    with pytest.raises(ValueError):
        gaussian_filter([[300]])


def test_invalid_image_dimension():
    with pytest.raises(ValueError):
        weighted_mean_filter([10, 20, 30])
