"""H02 — Patterning: một pixel thành một mẫu 2×2 hoặc 4×4."""

from demo_io import flat, png, read_gray, read_json, run, size
from e05_quantize import nearest

# Ma trận là thứ tự thêm chấm đen; ma trận Bayer là một ví dụ thứ tự cố định.
ORDER_2 = [[0, 2], [3, 1]]
ORDER_4 = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def pattern(pixels, order=ORDER_2):
    width, height = size(pixels)
    n = len(order)
    result = [[255] * (width * n) for _ in range(height * n)]
    for y, row in enumerate(pixels):
        for x, value in enumerate(row):
            black_count = nearest((255 - value) * n * n / 255)
            for r in range(n):
                for c in range(n):
                    if order[r][c] < black_count:
                        result[y * n + r][x * n + c] = 0
    return result


def read(path):
    if path.suffix.lower() != ".json":
        return {"pixels": read_gray(path)}
    data = read_json(path)
    return data if isinstance(data, dict) else {"pixels": data}


def demo(data, folder):
    pixels = data["pixels"]
    cell = data.get("cell", 2)
    if cell not in (2, 4):
        raise ValueError("cell phải bằng 2 hoặc 4")
    order = ORDER_2 if cell == 2 else ORDER_4
    result = pattern(pixels, order)
    png(folder / "pattern.png", result)
    return {"input_size": size(pixels), "output_size": size(result), "order": order,
            "levels": sorted(set(flat(result))),
            "preview": [row[:12] for row in result[:8]]}


if __name__ == "__main__":
    run("h02", __doc__, {"pixels": [[255, 128, 0]]}, demo, read)
