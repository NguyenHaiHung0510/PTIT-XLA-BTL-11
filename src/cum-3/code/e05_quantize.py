"""E05 — Lượng tử hóa: chia hệ số theo từng ô và làm tròn."""

from math import copysign, floor

from demo_io import run, size

LUMA = [
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99],
]


def nearest(value):
    # Giá trị đúng nửa đơn vị làm tròn ra xa 0: ±2.5 -> ±3.
    return int(copysign(floor(abs(value) + 0.5), value))


def quantize(coefficients, steps):
    if size(coefficients) != size(steps) or any(step <= 0 for row in steps for step in row):
        raise ValueError("Bảng lượng tử phải cùng kích thước và có bước dương")
    return [[nearest(value / step) for value, step in zip(row, qrow)]
            for row, qrow in zip(coefficients, steps)]


def dequantize(numbers, steps):
    return [[value * step for value, step in zip(row, qrow)]
            for row, qrow in zip(numbers, steps)]


def demo(data, folder):
    coefficients = data["coefficients"]
    steps = data.get("steps", LUMA)
    q = quantize(coefficients, steps)
    restored = dequantize(q, steps)
    return {"dct": coefficients, "steps": steps, "quantized": q, "dequantized": restored,
            "loss_of_precision": coefficients != restored}


if __name__ == "__main__":
    tiny = {"coefficients": [[25, -25], [5, -4]], "steps": [[10, 10], [10, 10]]}
    run("e05", __doc__, tiny, demo)
