"""E06 — Zig-zag: đi qua các đường chéo đổi chiều, bắt đầu ở DC."""

from demo_io import run, size


def coordinates(width, height):
    for diagonal in range(width + height - 1):
        first = max(0, diagonal - width + 1)
        last = min(diagonal, height - 1)
        rows = range(last, first - 1, -1) if diagonal % 2 == 0 else range(first, last + 1)
        for row in rows:
            yield row, diagonal - row


def scan(matrix):
    return [matrix[row][col] for row, col in coordinates(*size(matrix))]


def restore(numbers, width, height):
    if len(numbers) != width * height:
        raise ValueError("Số hệ số không khớp kích thước block")
    matrix = [[0] * width for _ in range(height)]
    for (row, col), value in zip(coordinates(width, height), numbers):
        matrix[row][col] = value
    return matrix


def demo(matrix, folder):
    numbers = scan(matrix)
    restored = restore(numbers, *size(matrix))
    return {"matrix": matrix, "zigzag": numbers, "restored": restored,
            "round_trip": matrix == restored}


if __name__ == "__main__":
    run("e06", __doc__, [[1, 2, 3], [4, 5, 6], [7, 8, 9]], demo)
