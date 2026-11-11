
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from A05 import gamma_transform


def test_gamma_identity():
    image = np.array([[0, 50, 128, 255]])

    np.testing.assert_array_equal(
        gamma_transform(image, 1), image
    )


def test_gamma_brighten():
    assert gamma_transform([[64]], 0.5)[0, 0] == 128


def test_gamma_darken():
    assert gamma_transform([[128]], 2)[0, 0] == 64


def test_endpoints():
    np.testing.assert_array_equal(
        gamma_transform([[0, 255]], 0.5),
        [[0, 255]]
    )


def test_invalid_gamma():
    with pytest.raises(ValueError):
        gamma_transform([[100]], 0)


def test_invalid_pixel():
    with pytest.raises(ValueError):
        gamma_transform([[300]], 2)


def test_invalid_dimension():
    with pytest.raises(ValueError):
        gamma_transform([10, 20], 2)
