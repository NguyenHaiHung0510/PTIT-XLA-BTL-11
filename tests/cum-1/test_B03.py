
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from B03 import k_nearest_mean_filter


def test_slide_example():
    image = [
        [1, 2, 3, 2],
        [4, 16, 2, 1],
        [4, 2, 1, 1],
        [2, 1, 2, 1]
    ]

    result = k_nearest_mean_filter(image, 3, 2, 3)

    assert result[1, 1] == 8


def test_keep_center_within_threshold():
    image = np.full((3, 3), 100)

    result = k_nearest_mean_filter(image, 3, 2)

    assert result[1, 1] == 100


def test_tie_prefers_larger():
    image = [
        [4, 6, 4],
        [6, 5, 4],
        [4, 4, 4]
    ]

    # Gan 5 nhat: 5, sau do 6 (uu tien 6 hon 4)
    result = k_nearest_mean_filter(image, k=2, theta=0)

    assert result[1, 1] == 6


def test_k_one_identity():
    image = np.array([
        [10, 20],
        [30, 40]
    ])

    np.testing.assert_array_equal(
        k_nearest_mean_filter(image, k=1),
        image
    )


def test_zero_padding():
    # Voi anh 1x1, ngoai anh la 0
    result = k_nearest_mean_filter(
        [[90]], k=3, theta=2, kernel_size=3
    )

    # Chon 90, 0, 0 -> trung binh = 30
    np.testing.assert_array_equal(result, [[30]])


def test_output_shape():
    image = np.full((4, 5), 100)

    assert k_nearest_mean_filter(image).shape == image.shape


def test_invalid_k():
    with pytest.raises(ValueError):
        k_nearest_mean_filter([[100]], k=10)


def test_invalid_theta():
    with pytest.raises(ValueError):
        k_nearest_mean_filter([[100]], theta=-1)


def test_invalid_kernel():
    with pytest.raises(ValueError):
        k_nearest_mean_filter([[100]], kernel_size=4)


def test_invalid_pixel():
    with pytest.raises(ValueError):
        k_nearest_mean_filter([[300]])


def test_invalid_dimension():
    with pytest.raises(ValueError):
        k_nearest_mean_filter([10, 20, 30])
