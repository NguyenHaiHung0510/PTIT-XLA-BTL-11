
import sys
from pathlib import Path
import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from A01 import negative


def test_negative():
    image = np.array([[0, 50, 255]])
    expected = np.array([[255, 205, 0]])

    np.testing.assert_array_equal(
        negative(image), expected
    )


def test_negative_twice():
    image = np.array([[10, 100, 200]])

    np.testing.assert_array_equal(
        negative(negative(image)), image
    )


def test_invalid_pixel():
    with pytest.raises(ValueError):
        negative(np.array([[300]]))
