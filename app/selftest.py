"""Tự kiểm tra lớp bọc. Chạy từ gốc repo:  python app/selftest.py

1. Chạy cả 50 thuật toán với tham số mặc định, kiểm tra đầu ra là ảnh uint8.
2. So khớp từng pixel: lớp bọc phải cho kết quả giống hệt hàm gốc trong src/.
3. Kiểm lại ví dụ slide C3 tr.52 (lọc k giá trị gần nhất: 16 → 8).
"""

import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import algorithms as alg  # noqa: E402
import samples  # noqa: E402
from A01 import negative  # noqa: E402
from A08 import equalize_histogram  # noqa: E402
from B03 import k_nearest_mean_filter  # noqa: E402
from B04 import median_filter  # noqa: E402
import edges  # noqa: E402
import h05_floyd_steinberg  # noqa: E402
import morphology  # noqa: E402


def main(size=64):
    gray = samples.make_sample("Hình khối + nhiễu muối tiêu", size)
    color = samples.make_sample("Hình khối", size, color=True)
    failures = 0

    print(f"1) Chạy {len(alg.ALGORITHMS)} thuật toán trên ảnh {size}×{size}")
    for algorithm in alg.ALGORITHMS:
        image = color if algorithm.color else gray
        params = {p.key: p.default for p in algorithm.params}
        started = time.perf_counter()
        try:
            result = alg.execute(algorithm, image, params)
        except Exception as error:
            failures += 1
            print(f"   LỖI {algorithm.code}: {type(error).__name__}: {error}")
            continue
        print(f"   OK  {algorithm.code} -> {result.image.shape} ({time.perf_counter() - started:.2f}s)")

    print("2) So khớp với hàm gốc")
    binary = (gray > 128).astype(np.uint8)
    cases = [
        ("A01", {}, negative(gray)),
        ("A08", {}, equalize_histogram(gray)[0].astype(np.uint8)),
        ("B03", {"k": 3, "theta": 2, "kernel_size": 3}, k_nearest_mean_filter(gray, 3, 2, 3)),
        ("B04", {"kernel_size": 5}, median_filter(gray, 5)),
        ("C04", {"magnitude": "l1", "T": 300}, edges.sobel(gray, "l1", 300)["edges"]),
        ("C07", {"low": 100, "high": 200}, edges.canny(gray, 100, 200)["edges"]),
        ("F01", {"se": "Vuông 3×3", "binarize": "Ngưỡng tự chọn", "T": 128, "invert": False},
         morphology.erosion(binary, np.ones((3, 3), np.uint8)) * 255),
        ("H05", {"cutoff": 127},
         np.array(h05_floyd_steinberg.diffuse(gray.tolist(), 127)[0], np.uint8)),
    ]
    for code, params, expected in cases:
        same = np.array_equal(alg.execute(alg.get(code), gray, params).image, expected)
        failures += not same
        print(f"   {'OK ' if same else 'LỆCH'} {code}")

    slide = np.array([[1, 2, 3, 2], [4, 16, 2, 1], [4, 2, 1, 1], [2, 1, 2, 1]], np.uint8)
    value = alg.execute(alg.get("B03"), slide, {"k": 3, "theta": 2, "kernel_size": 3}).image[1, 1]
    failures += value != 8
    print(f"3) Ví dụ C3 tr.52: pixel tâm 16 -> {value} ({'OK' if value == 8 else 'SAI'})")

    print("KẾT QUẢ:", "ĐẠT" if failures == 0 else f"{failures} lỗi")
    return failures


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
