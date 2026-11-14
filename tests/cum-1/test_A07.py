
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from A07 import (
    histogram,
    histogram_probability,
    transform_histogram
)


def test_histogram():
    image = [[0, 1, 1], [2, 2, 2]]

    np.testing.assert_array_equal(
        histogram(image, 4),
        [1, 2, 3, 0]
    )


def test_histogram_probability():
    result = histogram_probability(
        [[0, 1], [1, 1]], 2
    )

    np.testing.assert_allclose(
        result, [0.25, 0.75]
    )


def test_histogram_sum():
    image = [[0, 2, 3], [2, 3, 3]]

    assert histogram(image, 4).sum() == 6


def test_transform():
    image = [[0, 1, 2]]

    transformed, counts = transform_histogram(
        image, lambda g: abs(g - 2), 3
    )

    np.testing.assert_array_equal(
        transformed, [[2, 1, 0]]
    )
    np.testing.assert_array_equal(
        counts, [1, 1, 1]
    )


def test_merge_gray_levels():
    image = [[0, 1, 2, 3]]

    transformed, counts = transform_histogram(
        image, lambda g: g // 2, 4
    )

    np.testing.assert_array_equal(
        transformed, [[0, 0, 1, 1]]
    )
    np.testing.assert_array_equal(
        counts, [2, 2, 0, 0]
    )


def test_invalid_pixel():
    with pytest.raises(ValueError):
        histogram([[10]], 10)


def test_invalid_mapping():
    with pytest.raises(ValueError):
        transform_histogram(
            [[1]], lambda g: 100, 10
        )
