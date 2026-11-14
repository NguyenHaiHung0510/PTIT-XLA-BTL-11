
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from B01 import mean_filter


def test_center_slide():
    image = np.array([
        [104, 100, 108],
        [99, 106, 98],
        [95, 90, 85]
    ])

    result = mean_filter(image)

    # Trung binh = 98.3333, lam tron = 98
    assert result[1, 1] == 98


def test_zero_padding():
    image = [[90]]

    # Mot pixel 90, 8 vi tri padding bang 0
    np.testing.assert_array_equal(
        mean_filter(image, 3), [[10]]
    )


def test_uniform_image_center():
    image = np.full((5, 5), 90)

    assert mean_filter(image, 3)[2, 2] == 90


def test_kernel_5():
    image = np.full((5, 5), 100)

    assert mean_filter(image, 5)[2, 2] == 100


def test_shape():
    image = np.ones((4, 6))

    assert mean_filter(image).shape == (4, 6)


def test_invalid_kernel():
    with pytest.raises(ValueError):
        mean_filter([[100]], 4)


def test_invalid_pixel():
    with pytest.raises(ValueError):
        mean_filter([[300]])


def test_invalid_dimension():
    with pytest.raises(ValueError):
        mean_filter([1, 2, 3])


def test_empty_image():
    with pytest.raises(ValueError):
        mean_filter(np.empty((0, 0)))
