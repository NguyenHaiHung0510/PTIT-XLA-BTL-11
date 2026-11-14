
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from A04 import log_transform, inverse_log_transform


def test_log_endpoints():
    image = [[0, 255]]
    expected = [[0, 255]]

    np.testing.assert_array_equal(
        log_transform(image), expected
    )


def test_inverse_endpoints():
    np.testing.assert_array_equal(
        inverse_log_transform([[0, 255]]),
        [[0, 255]]
    )


def test_log_midpoint():
    # log(16)/log(256) = 0.5
    np.testing.assert_array_equal(
        log_transform([[15]]),
        [[128]]
    )


def test_inverse_midpoint():
    np.testing.assert_array_equal(
        inverse_log_transform([[128]]),
        [[15]]
    )


def test_log_brightens():
    assert log_transform([[50]])[0, 0] > 50


def test_inverse_darkens():
    assert inverse_log_transform([[200]])[0, 0] < 200


def test_invalid_pixel():
    with pytest.raises(ValueError):
        log_transform([[300]])


def test_invalid_dimension():
    with pytest.raises(ValueError):
        inverse_log_transform([1, 2, 3])
