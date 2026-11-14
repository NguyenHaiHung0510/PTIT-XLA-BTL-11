
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from A08 import equalize_histogram


def test_histogram():
    image = [[0, 1], [1, 2]]
    _, hist, _, _ = equalize_histogram(image, 3)

    np.testing.assert_array_equal(hist, [1, 2, 1])


def test_cdf():
    image = [[0, 1], [1, 2]]
    _, _, cdf, _ = equalize_histogram(image, 3)

    np.testing.assert_allclose(cdf, [0.25, 0.75, 1.0])


def test_mapping():
    image = [[0, 1], [1, 2]]
    _, _, _, mapping = equalize_histogram(image, 3)

    np.testing.assert_array_equal(mapping, [1, 2, 2])


def test_output_shape():
    image = np.array([[0, 1], [2, 3]])
    result, _, _, _ = equalize_histogram(image, 4)

    assert result.shape == image.shape


def test_preserve_pixel_count():
    image = [[0, 1, 2], [2, 3, 3]]
    result, _, _, _ = equalize_histogram(image, 4)

    assert result.size == 6


def test_monotonic_mapping():
    _, _, _, mapping = equalize_histogram(
        [[0, 1, 2, 3]], 4
    )

    assert np.all(np.diff(mapping) >= 0)


def test_invalid_pixel():
    with pytest.raises(ValueError):
        equalize_histogram([[10]], 6)


def test_invalid_levels():
    with pytest.raises(ValueError):
        equalize_histogram([[0]], 1)


def test_empty_image():
    with pytest.raises(ValueError):
        equalize_histogram(np.empty((0, 0)), 6)
