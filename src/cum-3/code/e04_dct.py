"""E04 — DCT/IDCT 2D: đổi giữa pixel và trọng số các mẫu cosine."""

from functools import lru_cache
from math import cos, pi, sqrt

from demo_io import read_gray, run, size


@lru_cache
def cosine_basis(n):
    return [[sqrt((1 if u == 0 else 2) / n) * cos(pi * (2 * x + 1) * u / (2 * n))
             for x in range(n)] for u in range(n)]


def transpose(matrix):
    return list(zip(*matrix))


def multiply(left, right):
    columns = transpose(right)
    return [[sum(a * b for a, b in zip(row, col)) for col in columns] for row in left]


def dct_1d(values):
    return [sum(a * v for a, v in zip(row, values)) for row in cosine_basis(len(values))]


def idct_1d(coefficients):
    basis = transpose(cosine_basis(len(coefficients)))
    return [sum(a * v for a, v in zip(row, coefficients)) for row in basis]


def dct(block):
    width, height = size(block)
    if width != height:
        raise ValueError("DCT demo dùng block vuông")
    basis = cosine_basis(width)
    coefficients = multiply(multiply(basis, block), transpose(basis))
    # DC = tổng pixel / N; tránh sai số sqrt khiến một tie lượng tử bị lệch.
    coefficients[0][0] = sum(sum(row) for row in block) / width
    return coefficients


def idct(coefficients):
    basis = cosine_basis(len(coefficients))
    return multiply(multiply(transpose(basis), coefficients), basis)


def display(matrix):
    return [[round(value, 6) for value in row] for row in matrix]


def read_block(path):
    rows = read_gray(path)
    if path.suffix.lower() != ".json":
        width, height = size(rows)
        n = min(width, height, 8)
        return [row[:n] for row in rows[:n]]
    return rows


def demo(block, folder):
    coefficients = dct(block)
    restored = idct(coefficients)
    error = max(abs(a - b) for row, back in zip(block, restored) for a, b in zip(row, back))
    return {"block": block, "dct": display(coefficients), "idct": display(restored),
            "first_row_dct_1d": [round(x, 6) for x in dct_1d(block[0])],
            "max_error": error}


if __name__ == "__main__":
    run("e04", __doc__, [[60, 100], [80, 110]], demo, read_block)
