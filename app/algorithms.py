"""Lớp bọc chung cho giao diện demo.

Mọi thuật toán được đưa về cùng một dạng:

    run(ảnh_uint8, **tham_số) -> Result(image=ảnh_uint8, info=..., extras=...)

Các hàm trong src/ được gọi NGUYÊN TRẠNG. Lớp bọc chỉ chuẩn bị đầu vào
(đổi kiểu, tính histogram, nhị phân hóa, chia khối 8x8...) và đổi đầu ra
thành ảnh để hiển thị. Không có dòng logic nào trong src/ bị sửa.
"""

from __future__ import annotations

import math
import sys
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List, Optional, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
for _sub in ("src/cum-1", "src/cum-2", "src/cum-3/code"):
    _path = str(ROOT / _sub)
    if _path not in sys.path:
        sys.path.insert(0, _path)

# Cụm 1: biến đổi điểm, histogram, lọc
from A01 import negative  # noqa: E402
from A02 import adjust_brightness  # noqa: E402
from A03 import threshold as fixed_threshold  # noqa: E402
from A04 import inverse_log_transform, log_transform  # noqa: E402
from A05 import gamma_transform  # noqa: E402
from A06 import contrast_stretch  # noqa: E402
from A07 import histogram as count_histogram, transform_histogram  # noqa: E402
from A08 import equalize_histogram  # noqa: E402
from B01 import mean_filter  # noqa: E402
from B02 import gaussian_filter, weighted_mean_filter  # noqa: E402
from B03 import k_nearest_mean_filter  # noqa: E402
from B04 import median_filter  # noqa: E402
from B05 import min_filter  # noqa: E402
from B06 import max_filter  # noqa: E402
from B07 import midpoint_filter  # noqa: E402

# Cụm 2: biên, phân vùng, hình thái
import edges  # noqa: E402
import morphology  # noqa: E402
import segmentation as seg  # noqa: E402

# Cụm 3: nén ảnh, màu, in ảnh
import e01_rlc  # noqa: E402
import e02_huffman  # noqa: E402
import e03_lzw  # noqa: E402
import e04_dct  # noqa: E402
import e05_quantize  # noqa: E402
import e06_zigzag  # noqa: E402
import e07_dpcm  # noqa: E402
import e08_ac_rle  # noqa: E402
import e09_jpeg_demo  # noqa: E402
import h01_rgb_cmy  # noqa: E402
import h02_patterning  # noqa: E402
import h03_ordered_dither  # noqa: E402
import h04_error_diffusion_1d  # noqa: E402
import h05_floyd_steinberg  # noqa: E402


# ---------------------------------------------------------------------------
# Kiểu dữ liệu chung
# ---------------------------------------------------------------------------

@dataclass
class Result:
    """Kết quả chung: ảnh chính, thông tin số và các ảnh trung gian."""

    image: np.ndarray
    info: dict = field(default_factory=dict)
    extras: List[Tuple[str, np.ndarray]] = field(default_factory=list)


@dataclass
class Param:
    key: str
    label: str
    kind: str  # "slider" | "select" | "check"
    default: object
    options: tuple = ()
    min: object = 0
    max: object = 1
    step: object = 1
    help: Optional[str] = None


@dataclass
class Algorithm:
    code: str
    name: str
    group: str
    run: Callable[..., Result]
    params: List[Param] = field(default_factory=list)
    source: str = ""
    note: str = ""
    color: bool = False  # True: nhận ảnh RGB thay vì ảnh xám
    max_size: Optional[int] = None  # giới hạn cạnh dài riêng cho bài chạy chậm


def slider(key, label, lo, hi, default, step=1, help=None):
    return Param(key, label, "slider", default, min=lo, max=hi, step=step, help=help)


def select(key, label, options, default=None, help=None):
    options = tuple(options)
    return Param(key, label, "select", options[0] if default is None else default,
                 options=options, help=help)


def check(key, label, default=False, help=None):
    return Param(key, label, "check", default, help=help)


# ---------------------------------------------------------------------------
# Tiện ích hiển thị (chỉ đổi dạng dữ liệu, không thuộc logic thuật toán)
# ---------------------------------------------------------------------------

def to_uint8(values):
    """Làm tròn .5 lên rồi cắt về 0..255."""
    values = np.asarray(values, dtype=np.float64)
    return np.clip(np.floor(values + 0.5), 0, 255).astype(np.uint8)


def stretch(values):
    """Co giãn tuyến tính min..max về 0..255 để nhìn được."""
    values = np.asarray(values, dtype=np.float64)
    low, high = float(values.min()), float(values.max())
    if high - low < 1e-12:
        return np.zeros(values.shape, dtype=np.uint8)
    return to_uint8((values - low) * 255.0 / (high - low))


def scale_by_max(values):
    """Lấy |giá trị| rồi chia cho giá trị lớn nhất, 0 giữ là đen."""
    values = np.abs(np.asarray(values, dtype=np.float64))
    peak = float(values.max())
    if peak < 1e-12:
        return np.zeros(values.shape, dtype=np.uint8)
    return to_uint8(values * 255.0 / peak)


def binary_image(mask):
    return (np.asarray(mask) > 0).astype(np.uint8) * 255


def to_rgb(gray):
    gray = np.asarray(gray, dtype=np.uint8)
    return gray.copy() if gray.ndim == 3 else np.stack([gray] * 3, axis=-1)


def overlay(gray, mask, color=(255, 40, 40), alpha=0.55):
    rgb = to_rgb(gray).astype(np.float64)
    mask = np.asarray(mask, dtype=bool)
    rgb[mask] = (1 - alpha) * rgb[mask] + alpha * np.array(color, dtype=np.float64)
    return to_uint8(rgb)


def boundaries(labels):
    labels = np.asarray(labels)
    edge = np.zeros(labels.shape, dtype=bool)
    edge[:, :-1] |= labels[:, :-1] != labels[:, 1:]
    edge[:-1, :] |= labels[:-1, :] != labels[1:, :]
    return edge


def regions_view(image, labels):
    """Tô mỗi vùng bằng mức xám trung bình của nó, vẽ biên vùng màu đỏ."""
    labels = np.asarray(labels)
    mean = np.zeros(image.shape, dtype=np.float64)
    for label in np.unique(labels):
        mask = labels == label
        mean[mask] = image[mask].mean()
    view = to_rgb(to_uint8(mean))
    view[boundaries(labels)] = (255, 40, 40)
    return view


def resize_to(image, width, height):
    return np.asarray(Image.fromarray(image).resize((int(width), int(height)), Image.BILINEAR))


def fit_max_side(image, max_side):
    """Thu nhỏ (giữ tỉ lệ) để cạnh dài không vượt max_side."""
    height, width = image.shape[:2]
    scale = max_side / max(height, width)
    if scale >= 1:
        return image
    return resize_to(image, max(1, round(width * scale)), max(1, round(height * scale)))


def chart_image(series, title, vline=None, ylabel="Số pixel", xlabel="Mức xám"):
    """Vẽ biểu đồ đường thành ảnh RGB (dùng cho histogram, bảng ánh xạ)."""
    fig, ax = plt.subplots(figsize=(6.4, 3.4), dpi=100)
    for name, values in series.items():
        values = np.asarray(values, dtype=np.float64)
        ax.plot(np.arange(len(values)), values, label=name, linewidth=1.2)
    if vline is not None:
        ax.axvline(vline, color="red", linestyle="--", linewidth=1.2, label=f"T = {vline:g}")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.canvas.draw()
    image = np.asarray(fig.canvas.buffer_rgba())[..., :3].copy()
    plt.close(fig)
    return image


def label_equal_regions(values):
    """Gán nhãn các vùng liên thông 4 có cùng giá trị (dùng để chuẩn bị đầu vào)."""
    values = np.asarray(values)
    height, width = values.shape
    labels = np.full((height, width), -1, dtype=np.int64)
    count = 0
    for r in range(height):
        for c in range(width):
            if labels[r, c] >= 0:
                continue
            value = values[r, c]
            labels[r, c] = count
            queue = deque([(r, c)])
            while queue:
                y, x = queue.popleft()
                for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                    if (0 <= ny < height and 0 <= nx < width
                            and labels[ny, nx] < 0 and values[ny, nx] == value):
                        labels[ny, nx] = count
                        queue.append((ny, nx))
            count += 1
    return labels, count


def _position(percent, length):
    return int(round(float(percent) / 100.0 * (length - 1)))


def _mark(view, row, col, color=(40, 220, 40)):
    view[max(0, row - 2):row + 3, col] = color
    view[row, max(0, col - 2):col + 3] = color
    return view


def _fmt(value):
    if isinstance(value, float):
        return round(value, 4)
    return value


# ---------------------------------------------------------------------------
# A. Biến đổi điểm và histogram (cụm 1)
# ---------------------------------------------------------------------------

def run_a01(img):
    return Result(negative(img))


def run_a02(img, c=1.5):
    return Result(adjust_brightness(img, float(c)), {"c": c})


def run_a03(img, T=127):
    return Result(fixed_threshold(img, T=T, max_value=255), {"T": T})


def run_a04(img, mode="Log"):
    fn = log_transform if mode == "Log" else inverse_log_transform
    return Result(fn(img), {"c": round(255 / math.log1p(255), 4)})


def run_a05(img, gamma=0.5):
    return Result(gamma_transform(img, float(gamma)), {"gamma": gamma})


def run_a06(img, r1=80, s1=30, r2=160, s2=220):
    out = contrast_stretch(img, r1=r1, s1=s1, r2=r2, s2=s2)
    lut = contrast_stretch(np.arange(256, dtype=np.uint8).reshape(1, -1), r1, s1, r2, s2)[0]
    chart = chart_image({"s = T(r)": lut}, "Hàm biến đổi theo đoạn", ylabel="Mức xám ra", xlabel="Mức xám vào")
    return Result(out, {"(r1, s1)": (r1, s1), "(r2, s2)": (r2, s2)}, [("Đồ thị hàm biến đổi", chart)])


A07_MAPPINGS = ("|g − a|", "|2g − 255|")


def run_a07(img, mapping=A07_MAPPINGS[0], a=128):
    functions = {A07_MAPPINGS[0]: lambda g: abs(g - int(a)),
                 A07_MAPPINGS[1]: lambda g: abs(2 * g - 255)}
    transformed, new_hist = transform_histogram(img, functions[mapping])
    old_hist = count_histogram(img)
    chart = chart_image({"h(g) ảnh gốc": old_hist, "h'(g) sau biến đổi": new_hist},
                        "Histogram trước / sau biến đổi")
    shown = f"|g − {a}|" if mapping == A07_MAPPINGS[0] else mapping
    return Result(transformed.astype(np.uint8), {"f(g)": shown}, [("Histogram", chart)])


def run_a08(img):
    result, hist, cdf, mapping = equalize_histogram(img)
    result = result.astype(np.uint8)
    chart = chart_image({"Trước cân bằng": hist, "Sau cân bằng": count_histogram(result)},
                        "Histogram trước / sau")
    lut = chart_image({"s = (L−1)·CDF(r)": mapping}, "Bảng ánh xạ mức xám",
                      ylabel="Mức xám ra", xlabel="Mức xám vào")
    used = int(np.count_nonzero(hist))
    return Result(result, {"Số mức xám có pixel": used},
                  [("Histogram", chart), ("Bảng ánh xạ", lut)])


# ---------------------------------------------------------------------------
# B. Lọc ảnh (cụm 1)
# ---------------------------------------------------------------------------

def run_b01(img, kernel_size=3):
    return Result(mean_filter(img, kernel_size))


B02_KINDS = ("Trung bình trọng số 3×3", "Gaussian 5×5")


def run_b02(img, kind=B02_KINDS[0]):
    fn = weighted_mean_filter if kind == B02_KINDS[0] else gaussian_filter
    return Result(fn(img))


def run_b03(img, k=3, theta=2, kernel_size=3):
    return Result(k_nearest_mean_filter(img, k=int(k), theta=theta, kernel_size=kernel_size))


def run_b04(img, kernel_size=3):
    return Result(median_filter(img, kernel_size))


def run_b05(img, kernel_size=3):
    return Result(min_filter(img, kernel_size))


def run_b06(img, kernel_size=3):
    return Result(max_filter(img, kernel_size))


def run_b07(img, kernel_size=3):
    return Result(midpoint_filter(img, kernel_size))


# ---------------------------------------------------------------------------
# C. Biên và làm sắc nét (cụm 2)
# ---------------------------------------------------------------------------

def _gradient(fn):
    def run(img, magnitude="l1", T=0):
        result = fn(img, magnitude=magnitude, threshold=(float(T) if T > 0 else None))
        strength = scale_by_max(result["magnitude"])
        extras = [("|Gx| (co giãn theo max)", scale_by_max(result["gx"])),
                  ("|Gy| (co giãn theo max)", scale_by_max(result["gy"]))]
        info = {"|G| lớn nhất": float(result["magnitude"].max())}
        if T > 0:
            info["T"] = T
            extras.insert(0, ("Độ lớn gradient (co giãn theo max)", strength))
            return Result(result["edges"], info, extras)
        return Result(strength, info, extras)
    return run


def run_c05(img, neighbors=4):
    response = edges.laplacian(img, neighbors)
    return Result(scale_by_max(response),
                  {"Đáp ứng nhỏ nhất": float(response.min()), "Đáp ứng lớn nhất": float(response.max())},
                  [("Đáp ứng có dấu (co giãn min–max)", stretch(response))])


def run_c06(img, neighbors=4):
    sharpened = edges.sharpen_laplacian(img, neighbors)
    clipped = int(np.count_nonzero((sharpened < 0) | (sharpened > 255)))
    return Result(to_uint8(sharpened), {"Số pixel bị cắt về 0..255": clipped},
                  [("Laplacian (co giãn theo max)", scale_by_max(edges.laplacian(img, neighbors)))])


def run_c07(img, low=100, high=200):
    result = edges.canny(img, float(low), float(high))
    return Result(result["edges"], {"Ngưỡng thấp T2": low, "Ngưỡng cao T1": high,
                                    "Số điểm biên": int(np.count_nonzero(result["edges"]))},
                  [("1. Làm mịn Gaussian", to_uint8(result["smoothed"])),
                   ("2. Độ lớn gradient Sobel", scale_by_max(result["magnitude"])),
                   ("3. Sau loại bỏ không cực đại", scale_by_max(result["suppressed"]))])


# ---------------------------------------------------------------------------
# D. Ngưỡng và phân vùng (cụm 2)
# ---------------------------------------------------------------------------

def _apply_threshold(img, hist, T, title, info):
    used = float(min(max(T, 0.0), 255.0))
    info = {"Ngưỡng T": float(T), **info}
    if used != T:
        info["Ghi chú"] = f"T nằm ngoài 0..255, đã cắt về {used:g} khi áp ngưỡng"
    out = fixed_threshold(img, T=used, max_value=255)
    return Result(out, info, [("Histogram và ngưỡng", chart_image({"h(g)": hist}, title, vline=used))])


def run_d01(img, window=5):
    hist = seg.histogram(img)
    smooth = seg.smooth_histogram(hist, int(window))
    chart = chart_image({"Histogram gốc": hist, f"Làm trơn W = {window}": smooth},
                        "Làm trơn histogram")
    return Result(chart, {"W": window, "Đỉnh gốc": int(np.argmax(hist)),
                          "Đỉnh sau làm trơn": int(np.argmax(smooth))},
                  [("Ảnh đầu vào", img)])


def run_d02(img):
    hist = seg.histogram(img)
    result = seg.otsu_threshold(hist)
    return _apply_threshold(img, hist, result["threshold"], "Otsu",
                            {"Các k cực đại": [int(k) for k in result["maxima"]]})


def run_d03(img):
    hist = seg.histogram(img)
    result = seg.isodata_threshold(hist)
    return _apply_threshold(img, hist, result["threshold"], "Isodata",
                            {"Số lần lặp": len(result["history"]) - 1,
                             "T0 (mức xám trung bình)": result["history"][0]})


def run_d04(img, percentile=95):
    hist = seg.histogram(img)
    result = seg.background_symmetry_threshold(hist, float(percentile))
    return _apply_threshold(img, hist, result["threshold"], "Đối xứng nền",
                            {"maxp (đỉnh nền)": result["peak"],
                             f"Mức tại {percentile}%": result["percentile_level"]})


def run_d05(img):
    hist = seg.histogram(img)
    result = seg.triangle_threshold(hist)
    return _apply_threshold(img, hist, result["threshold"], "Tam giác",
                            {"bmin": result["minimum"], "bmax (đỉnh)": result["peak"]})


def _range_predicate(tol):
    """P(R): chênh lệch max − min trong vùng không vượt tol."""
    return lambda values: bool(values.max() - values.min() <= tol)


def run_d06(img, seed_row=50, seed_col=50, tol=20, connectivity=4):
    height, width = img.shape
    seed = (_position(seed_row, height), _position(seed_col, width))
    mask = seg.region_growing(img, seed, lambda v, s: abs(v - s) <= tol, connectivity)
    view = _mark(overlay(img, mask), *seed)
    return Result(view, {"Seed (hàng, cột)": seed, "Mức xám seed": int(img[seed]),
                         "Số pixel trong vùng": int(mask.sum())},
                  [("Mặt nạ vùng", binary_image(mask))])


def run_d07(img, tol=20, size=48):
    small = fit_max_side(img, int(size))
    # Vùng khởi tạo: pixel liền kề cùng khoảng mức xám độ rộng tol+1, nên mỗi vùng thỏa P(R).
    initial, count = label_equal_regions(small // (int(tol) + 1))
    labels = seg.region_merging(small, initial, _range_predicate(tol))
    return Result(regions_view(small, labels),
                  {"Kích thước xử lý": f"{small.shape[1]}×{small.shape[0]}",
                   "Số vùng khởi tạo": count, "Số vùng sau khi hợp": int(labels.max()) + 1},
                  [("Vùng khởi tạo", regions_view(small, initial))])


def run_d08(img, tol=20, size=64):
    square = resize_to(img, size, size)
    result = seg.quadtree_split(square, _range_predicate(tol))
    labels = result["labels"]
    return Result(regions_view(square, labels),
                  {"Kích thước xử lý": f"{size}×{size}", "Số vùng lá": int(labels.max()) + 1},
                  [("Ảnh vuông đầu vào", square)])


def run_d09(img, tol=20, size=64):
    square = resize_to(img, size, size)
    result = seg.split_and_merge(square, _range_predicate(tol))
    return Result(regions_view(square, result["labels"]),
                  {"Kích thước xử lý": f"{size}×{size}",
                   "Số vùng sau tách": int(result["split_labels"].max()) + 1,
                   "Số vùng sau hợp": int(result["labels"].max()) + 1},
                  [("Sau pha tách (quadtree)", regions_view(square, result["split_labels"]))])


# ---------------------------------------------------------------------------
# F. Hình thái học (cụm 2)
# ---------------------------------------------------------------------------

SE_CHOICES = {
    "Vuông 3×3": np.ones((3, 3), dtype=np.uint8),
    "Chữ thập 3×3": morphology.CROSS_3,
    "Vuông 5×5": np.ones((5, 5), dtype=np.uint8),
}
BINARIZE = ("Otsu", "Ngưỡng tự chọn")


def _binarize(img, binarize, T, invert):
    if binarize == BINARIZE[0]:
        T = seg.otsu_threshold(seg.histogram(img))["threshold"]
    binary = fixed_threshold(img, T=float(T), max_value=1)
    if invert:
        binary = 1 - binary
    return binary.astype(np.uint8), float(T)


def _morph(operation):
    def run(img, se="Vuông 3×3", binarize=BINARIZE[0], T=127, invert=False):
        binary, used = _binarize(img, binarize, T, invert)
        out = operation(binary, SE_CHOICES[se])
        return Result(binary_image(out),
                      {"Ngưỡng nhị phân": used, "Pixel đối tượng trước": int(binary.sum()),
                       "Pixel đối tượng sau": int(out.sum())},
                      [("Ảnh nhị phân đầu vào", binary_image(binary))])
    return run


def find_hole_seeds(binary):
    """Mỗi vùng nền (0) không chạm mép ảnh là một lỗ; lấy một pixel làm seed."""
    labels, _ = label_equal_regions(binary)
    border = set(np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]])))
    seeds = []
    for label in np.unique(labels[binary == 0]):
        if label not in border:
            r, c = np.argwhere(labels == label)[0]
            seeds.append((int(r), int(c)))
    return seeds


SEED_MODES = ("Tự tìm các lỗ", "Chọn seed (%)")


def run_f05(img, binarize=BINARIZE[0], T=127, invert=False, seed_mode=SEED_MODES[0],
            seed_row=50, seed_col=50):
    binary, used = _binarize(img, binarize, T, invert)
    if seed_mode == SEED_MODES[0]:
        seeds = find_hole_seeds(binary)
        if not seeds:
            raise ValueError("Không tìm thấy lỗ (vùng nền bị đối tượng bao kín). "
                             "Thử bật 'Đảo nhị phân' hoặc đổi ngưỡng.")
    else:
        seeds = [(_position(seed_row, binary.shape[0]), _position(seed_col, binary.shape[1]))]
    result = morphology.hole_filling(binary, morphology.CROSS_3, seeds)
    return Result(binary_image(result["filled"]),
                  {"Ngưỡng nhị phân": used, "Số seed": len(seeds),
                   "Số pixel được lấp": int(result["holes"].sum()), "Số vòng lặp": result["iterations"]},
                  [("Ảnh nhị phân đầu vào", binary_image(binary)),
                   ("Phần được lấp (đỏ)", overlay(binary_image(binary), result["holes"], alpha=1.0))])


# ---------------------------------------------------------------------------
# E. Nén ảnh (cụm 3, các hàm nhận list Python)
# ---------------------------------------------------------------------------

LUMA = e05_quantize.LUMA


def _blocks(img):
    """Đệm mép cho đủ bội 8, trừ 128 như JPEG, trả các khối 8x8 dạng list."""
    pad_h, pad_w = (-img.shape[0]) % 8, (-img.shape[1]) % 8
    padded = np.pad(img.astype(np.int64), ((0, pad_h), (0, pad_w)), mode="edge") - 128
    positions, blocks = [], []
    for y in range(0, padded.shape[0], 8):
        for x in range(0, padded.shape[1], 8):
            positions.append((y, x))
            blocks.append(padded[y:y + 8, x:x + 8].tolist())
    return positions, blocks, padded.shape


def _assemble(positions, blocks, shape, crop):
    out = np.zeros(shape, dtype=np.float64)
    for (y, x), block in zip(positions, blocks):
        out[y:y + 8, x:x + 8] = np.asarray(block, dtype=np.float64)
    return out[:crop[0], :crop[1]]


def _quality(original, restored):
    diff = original.astype(np.float64) - restored.astype(np.float64)
    mse = float(np.mean(diff * diff))
    psnr = float("inf") if mse == 0 else 10 * math.log10(255 ** 2 / mse)
    return {"MAE": float(np.mean(np.abs(diff))), "PSNR (dB)": psnr}


def _steps(q_scale):
    return [[value * float(q_scale) for value in row] for row in LUMA]


def _reconstruct(positions, coefficient_blocks, shape, crop):
    blocks = [e04_dct.idct(block) for block in coefficient_blocks]
    return to_uint8(_assemble(positions, blocks, shape, crop) + 128)


def run_e01(img):
    rows = img.tolist()
    runs = [e01_rlc.encode_row(row) for row in rows]
    decoded = np.array([e01_rlc.decode_row(row) for row in runs], dtype=np.uint8)
    lengths = np.array([[count for count, _ in row for _ in range(count)] for row in runs])
    run_count = sum(map(len, runs))
    return Result(decoded, {"Số pixel": img.size, "Số loạt (độ dài, giá trị)": run_count,
                            "Tỉ lệ dữ liệu (2 × số loạt / số pixel)": 2 * run_count / img.size,
                            "Giải mã khớp ảnh gốc": bool(np.array_equal(decoded, img))},
                  [("Độ dài loạt tại mỗi pixel (sáng = loạt dài)", stretch(lengths))])


def run_e02(img):
    symbols = img.ravel().tolist()
    tree, counts, _ = e02_huffman.build_tree(symbols)
    table = e02_huffman.code_table(tree)
    bits = e02_huffman.encode(symbols, table)
    decoded = np.array(e02_huffman.decode(bits, tree), dtype=np.uint8).reshape(img.shape)
    lengths = np.zeros(256)
    for symbol, code in table.items():
        lengths[symbol] = len(code)
    bpp = len(bits) / img.size
    return Result(decoded, {"Số ký hiệu khác nhau": len(counts), "Số bit mã hóa": len(bits),
                            "Bit/pixel": bpp, "Tỉ số nén so với 8 bit": 8 / bpp,
                            "Giải mã khớp ảnh gốc": bool(np.array_equal(decoded, img))},
                  [("Độ dài mã Huffman tại mỗi pixel (sáng = mã dài)", stretch(lengths[img]))])


def run_e03(img):
    symbols = img.ravel().tolist()
    alphabet = list(range(256))
    codes, added = e03_lzw.encode(symbols, alphabet)
    decoded = np.array(e03_lzw.decode(codes, alphabet), dtype=np.uint8).reshape(img.shape)
    width = math.ceil(math.log2(len(alphabet) + len(added)))
    return Result(decoded, {"Số mã phát ra": len(codes), "Số mục thêm vào từ điển": len(added),
                            "Độ rộng mã cố định (bit)": width,
                            "Tỉ số nén ước tính": img.size * 8 / (len(codes) * width),
                            "Giải mã khớp ảnh gốc": bool(np.array_equal(decoded, img))})


def run_e04(img):
    positions, blocks, shape = _blocks(img)
    coefficients = [e04_dct.dct(block) for block in blocks]
    restored = _reconstruct(positions, coefficients, shape, img.shape)
    coefficient_map = _assemble(positions, coefficients, shape, img.shape)
    return Result(stretch(np.log1p(np.abs(coefficient_map))),
                  {"Số khối 8×8": len(blocks), "DC khối đầu": coefficients[0][0][0],
                   "Sai số lớn nhất sau IDCT": int(np.max(np.abs(restored.astype(int) - img)))},
                  [("Ảnh dựng lại bằng IDCT", restored)])


def run_e05(img, q_scale=1.0):
    positions, blocks, shape = _blocks(img)
    steps = _steps(q_scale)
    quantized = [e05_quantize.quantize(e04_dct.dct(block), steps) for block in blocks]
    restored = _reconstruct(positions, [e05_quantize.dequantize(q, steps) for q in quantized],
                            shape, img.shape)
    zeros = sum(value == 0 for block in quantized for row in block for value in row)
    info = {"Hệ số nhân bảng lượng tử": q_scale, "Tỉ lệ hệ số bằng 0": zeros / (64 * len(blocks))}
    info.update(_quality(img, restored))
    return Result(restored, info,
                  [("Sai lệch |gốc − dựng lại| (co giãn)", stretch(np.abs(img.astype(int) - restored)))])


def run_e06(img, keep=10):
    positions, blocks, shape = _blocks(img)
    kept = []
    for block in blocks:
        vector = e06_zigzag.scan(e04_dct.dct(block))
        vector = vector[:keep] + [0] * (64 - keep)
        kept.append(e06_zigzag.restore(vector, 8, 8))
    restored = _reconstruct(positions, kept, shape, img.shape)
    order = np.array(e06_zigzag.restore(list(range(64)), 8, 8))
    order_view = np.kron(stretch(order), np.ones((24, 24), dtype=np.uint8))
    info = {"Số hệ số giữ lại mỗi khối": f"{keep}/64"}
    info.update(_quality(img, restored))
    return Result(restored, info, [("Thứ tự quét zig-zag (tối = quét trước)", order_view)])


def run_e07(img):
    positions, blocks, shape = _blocks(img)
    dc = [e05_quantize.nearest(e04_dct.dct(block)[0][0] / LUMA[0][0]) for block in blocks]
    differences = e07_dpcm.encode(dc)
    restored = e07_dpcm.decode(differences)
    # DC trực chuẩn = tổng/8 → trung bình khối = DC/8; nhân lại bước lượng tử 16.
    means = [[[value * LUMA[0][0] / 8] * 8] * 8 for value in restored]
    diff_map = [[[value] * 8] * 8 for value in differences]
    return Result(to_uint8(_assemble(positions, means, shape, img.shape) + 128),
                  {"Khoảng giá trị DC": (min(dc), max(dc)),
                   "Khoảng giá trị sai phân": (min(differences), max(differences)),
                   "Giải mã khớp DC": restored == dc},
                  [("Sai phân DC giữa các khối (co giãn)",
                    stretch(_assemble(positions, diff_map, shape, img.shape)))])


def run_e08(img, q_scale=1.0):
    positions, blocks, shape = _blocks(img)
    steps = _steps(q_scale)
    vectors = [e06_zigzag.scan(e05_quantize.quantize(e04_dct.dct(block), steps)) for block in blocks]
    pairs = [e08_ac_rle.encode(vector[1:]) for vector in vectors]
    decoded = [[vector[0]] + e08_ac_rle.decode(encoded, 63) for vector, encoded in zip(vectors, pairs)]
    coefficient_blocks = [e05_quantize.dequantize(e06_zigzag.restore(vector, 8, 8), steps)
                          for vector in decoded]
    restored = _reconstruct(positions, coefficient_blocks, shape, img.shape)
    info = {"Tổng số hệ số AC": 63 * len(blocks), "Số cặp (skip, value)": sum(map(len, pairs)),
            "Giải mã RLE khớp": decoded == vectors}
    info.update(_quality(img, restored))
    return Result(restored, info)


def run_e09(img):
    pixels = img.tolist()
    height, width = img.shape
    positions, blocks = e09_jpeg_demo.blocks_from(pixels)
    vectors = [e06_zigzag.scan(e05_quantize.quantize(e04_dct.dct(b), LUMA)) for b in blocks]
    tree, bits, _, _ = e09_jpeg_demo.entropy_encode(vectors)
    decoded = e09_jpeg_demo.entropy_decode(tree, bits)
    restored = np.array(e09_jpeg_demo.reconstruct(positions, decoded, width, height), dtype=np.uint8)
    info = {"Số khối 8×8": len(blocks), "Số bit payload": len(bits),
            "Bit/pixel": len(bits) / img.size, "Tỉ số nén so với 8 bit": img.size * 8 / len(bits),
            "Mã hóa/giải mã entropy khớp": decoded == vectors}
    info.update(_quality(img, restored))
    return Result(restored, info,
                  [("Sai lệch |gốc − dựng lại| (co giãn)", stretch(np.abs(img.astype(int) - restored)))])


# ---------------------------------------------------------------------------
# H. Màu và in ảnh (cụm 3)
# ---------------------------------------------------------------------------

def run_h01(img):
    cmy = h01_rgb_cmy.complement(img.tolist())
    restored = np.array(h01_rgb_cmy.complement(cmy), dtype=np.uint8)
    cmy = np.array(cmy, dtype=np.uint8)
    return Result(cmy, {"Pixel đầu RGB": img[0, 0].tolist(), "Pixel đầu CMY": cmy[0, 0].tolist(),
                        "RGB dựng lại khớp": bool(np.array_equal(restored, img))},
                  [("Kênh C (sáng = nhiều mực)", cmy[..., 0]), ("Kênh M", cmy[..., 1]),
                   ("Kênh Y", cmy[..., 2]), ("RGB dựng lại từ CMY", restored)])


def run_h02(img, cell=2):
    order = h02_patterning.ORDER_2 if cell == 2 else h02_patterning.ORDER_4
    out = np.array(h02_patterning.pattern(img.tolist(), order), dtype=np.uint8)
    return Result(out, {"Kích thước vào": f"{img.shape[1]}×{img.shape[0]}",
                        "Kích thước ra": f"{out.shape[1]}×{out.shape[0]}", "Ma trận thứ tự": order})


H03_MATRICES = {
    "Mặc định trong code (2×2)": h03_ordered_dither.THRESHOLDS,
    "Slide C4 tr.55 (2×2)": [[0, 60], [45, 110]],
    "Slide C4 tr.55 (4×4)": [[0, 128, 32, 160], [192, 64, 224, 96],
                             [48, 176, 16, 144], [240, 112, 208, 80]],
}


def run_h03(img, matrix="Mặc định trong code (2×2)"):
    thresholds = H03_MATRICES[matrix]
    out = np.array(h03_ordered_dither.dither(img.tolist(), thresholds), dtype=np.uint8)
    return Result(out, {"Ma trận ngưỡng": thresholds})


def run_h04(img, cutoff=127):
    rows = [h04_error_diffusion_1d.diffuse_row(row, cutoff)[0] for row in img.tolist()]
    baseline = [[h04_error_diffusion_1d.threshold(v, cutoff) for v in row] for row in img.tolist()]
    return Result(np.array(rows, dtype=np.uint8), {"Ngưỡng": cutoff},
                  [("Phân ngưỡng thường (không khuếch tán)", np.array(baseline, dtype=np.uint8))])


def run_h05(img, cutoff=127):
    out, _ = h05_floyd_steinberg.diffuse(img.tolist(), cutoff)
    baseline = [[h04_error_diffusion_1d.threshold(v, cutoff) for v in row] for row in img.tolist()]
    return Result(np.array(out, dtype=np.uint8), {"Ngưỡng": cutoff},
                  [("Phân ngưỡng thường (không khuếch tán)", np.array(baseline, dtype=np.uint8))])


# ---------------------------------------------------------------------------
# Bảng đăng ký
# ---------------------------------------------------------------------------

G_A = "A. Biến đổi điểm & histogram"
G_B = "B. Lọc ảnh"
G_C = "C. Biên & làm sắc nét"
G_D = "D. Ngưỡng & phân vùng"
G_E = "E. Nén ảnh"
G_F = "F. Hình thái học"
G_H = "H. Màu & in ảnh"

KERNEL = select("kernel_size", "Kích thước cửa sổ", (3, 5, 7))
MAGNITUDE = select("magnitude", "Độ lớn gradient", ("l1", "l2"),
                   help="l1 = |Gx| + |Gy|, l2 = √(Gx² + Gy²)")
EDGE_T = slider("T", "Ngưỡng biên T (0 = chỉ xem độ lớn)", 0, 1000, 0, 10)
NEIGHBORS = select("neighbors", "Mặt nạ Laplacian", (4, 8), help="4: tâm −4; 8: tâm −8")
TOL = slider("tol", "Tiêu chuẩn đồng nhất: max − min ≤", 0, 100, 20)
Q_SCALE = slider("q_scale", "Hệ số nhân bảng lượng tử", 0.5, 8.0, 1.0, 0.5)
CUTOFF = slider("cutoff", "Ngưỡng", 0, 255, 127)
MORPH_PARAMS = [
    select("se", "Phần tử cấu trúc", tuple(SE_CHOICES)),
    select("binarize", "Nhị phân hóa", BINARIZE),
    slider("T", "Ngưỡng tự chọn (khi không dùng Otsu)", 0, 255, 127),
    check("invert", "Đảo nhị phân (đối tượng là vùng tối)"),
]

ALGORITHMS = [
    Algorithm("A01", "Âm bản", G_A, run_a01, source="C3 tr.13"),
    Algorithm("A02", "Biến đổi tuyến tính độ sáng", G_A, run_a02,
              [slider("c", "Hệ số c (s = c·r)", 0.0, 3.0, 1.5, 0.1)], "C3 tr.18 (γ = 1)"),
    Algorithm("A03", "Phân ngưỡng cố định", G_A, run_a03,
              [slider("T", "Ngưỡng T", 0, 255, 127)], "C3 tr.14"),
    Algorithm("A04", "Biến đổi log / log ngược", G_A, run_a04,
              [select("mode", "Phép biến đổi", ("Log", "Log ngược"))], "C3 tr.15–17"),
    Algorithm("A05", "Biến đổi lũy thừa gamma", G_A, run_a05,
              [slider("gamma", "γ", 0.1, 5.0, 0.5, 0.1)], "C3 tr.18–20"),
    Algorithm("A06", "Kéo giãn tương phản theo đoạn", G_A, run_a06,
              [slider("r1", "r1", 1, 253, 80), slider("s1", "s1", 0, 255, 30),
               slider("r2", "r2", 2, 254, 160), slider("s2", "s2", 0, 255, 220)],
              "C3 tr.21", note="Cần 0 < r1 < r2 < 255 và s1 ≤ s2."),
    Algorithm("A07", "Histogram sau biến đổi mức xám", G_A, run_a07,
              [select("mapping", "Hàm f(g)", A07_MAPPINGS), slider("a", "a (cho |g − a|)", 0, 255, 128)],
              "C3 tr.23–31; câu 3.1, 3.2"),
    Algorithm("A08", "Cân bằng histogram", G_A, run_a08, source="C3 tr.32–38; câu 3.4, 3.5"),

    Algorithm("B01", "Lọc trung bình số học", G_B, run_b01, [KERNEL], "C3 tr.46–48"),
    Algorithm("B02", "Lọc trung bình có trọng số / Gaussian", G_B, run_b02,
              [select("kind", "Mặt nạ", B02_KINDS)], "C3 tr.49; C5 tr.40"),
    Algorithm("B03", "Lọc trung bình k giá trị gần nhất", G_B, run_b03,
              [slider("k", "k", 1, 25, 3), slider("theta", "Ngưỡng θ", 0, 50, 2),
               select("kernel_size", "Kích thước cửa sổ", (3, 5))],
              "C3 tr.50–52", note="Cần k ≤ (kích thước cửa sổ)²."),
    Algorithm("B04", "Lọc trung vị", G_B, run_b04, [KERNEL], "C3 tr.53–54"),
    Algorithm("B05", "Lọc min", G_B, run_b05, [KERNEL], "C3 tr.42, 71"),
    Algorithm("B06", "Lọc max", G_B, run_b06, [KERNEL], "C3 tr.42, 71"),
    Algorithm("B07", "Lọc điểm giữa (midpoint)", G_B, run_b07, [KERNEL], "C3 tr.69, 72"),

    Algorithm("C01", "Gradient sai phân 1D", G_C, _gradient(edges.gradient_1d),
              [MAGNITUDE, EDGE_T], "C5 tr.14–16"),
    Algorithm("C02", "Roberts", G_C, _gradient(edges.roberts), [MAGNITUDE, EDGE_T], "C5 tr.17"),
    Algorithm("C03", "Prewitt", G_C, _gradient(edges.prewitt), [MAGNITUDE, EDGE_T], "C5 tr.18–22"),
    Algorithm("C04", "Sobel", G_C, _gradient(edges.sobel), [MAGNITUDE, EDGE_T], "C5 tr.18–26"),
    Algorithm("C05", "Laplacian", G_C, run_c05, [NEIGHBORS], "C5 tr.28–30, 35"),
    Algorithm("C06", "Làm sắc nét bằng Laplacian", G_C, run_c06, [NEIGHBORS], "C5 tr.31–35"),
    Algorithm("C07", "Canny", G_C, run_c07,
              [slider("low", "Ngưỡng thấp T2", 0, 1000, 100, 10),
               slider("high", "Ngưỡng cao T1", 0, 1000, 200, 10)],
              "C5 tr.36–49", note="Cần T2 < T1. Ngưỡng tính trên độ lớn |Gx| + |Gy| thô."),

    Algorithm("D01", "Làm trơn histogram", G_D, run_d01,
              [select("window", "Cửa sổ W", (3, 5, 7, 9), 5)], "C5 tr.62; câu 3.3",
              note="Kết quả là ảnh biểu đồ histogram trước/sau làm trơn."),
    Algorithm("D02", "Ngưỡng Otsu", G_D, run_d02, source="C5 tr.65–70",
              note="Tìm T trên histogram rồi áp ngưỡng bằng A03."),
    Algorithm("D03", "Ngưỡng đẳng liệu (Isodata)", G_D, run_d03, source="C5 tr.71–75",
              note="Tìm T trên histogram rồi áp ngưỡng bằng A03."),
    Algorithm("D04", "Ngưỡng đối xứng nền", G_D, run_d04,
              [slider("percentile", "p (%)", 50, 100, 95)], "C5 tr.76–77, 79",
              note="Giả định nền sáng, đối tượng ở bên trái đỉnh histogram (như slide)."),
    Algorithm("D05", "Ngưỡng tam giác", G_D, run_d05, source="C5 tr.78",
              note="Xét phía trái đỉnh histogram (như slide)."),
    Algorithm("D06", "Phát triển vùng (region growing)", G_D, run_d06,
              [slider("seed_row", "Seed: hàng (% chiều cao)", 0, 100, 50),
               slider("seed_col", "Seed: cột (% chiều rộng)", 0, 100, 50),
               slider("tol", "|mức xám − seed| ≤", 0, 100, 20),
               select("connectivity", "Liên thông", (4, 8))], "C5 tr.85–86"),
    Algorithm("D07", "Hợp vùng (region merging)", G_D, run_d07,
              [TOL, select("size", "Cạnh dài khi xử lý (px)", (32, 48, 64), 48)], "C5 tr.87–88",
              note="Thuật toán chậm nên ảnh được thu nhỏ. Vùng khởi tạo: các pixel liền kề "
                   "cùng khoảng mức xám (độ rộng tol + 1)."),
    Algorithm("D08", "Tách vùng quadtree", G_D, run_d08,
              [TOL, select("size", "Kích thước ảnh vuông N×N", (32, 64, 128), 64)], "C5 tr.89–93",
              note="Ảnh được co về N×N, N là lũy thừa của 2 (yêu cầu ở C5 tr.91)."),
    Algorithm("D09", "Tách và hợp vùng", G_D, run_d09,
              [TOL, select("size", "Kích thước ảnh vuông N×N", (32, 64, 128), 64)], "C5 tr.94–100",
              note="Ảnh được co về N×N, N là lũy thừa của 2."),

    Algorithm("E01", "Mã loạt dài RLC", G_E, run_e01, source="C6 tr.11–13",
              note="Ảnh kết quả là ảnh giải mã (nén không tổn thất nên giống ảnh gốc)."),
    Algorithm("E02", "Mã Huffman", G_E, run_e02, source="C6 tr.14–22",
              note="Ảnh kết quả là ảnh giải mã (nén không tổn thất nên giống ảnh gốc)."),
    Algorithm("E03", "Mã LZW", G_E, run_e03, source="C6 tr.23–30",
              note="Ảnh kết quả là ảnh giải mã (nén không tổn thất nên giống ảnh gốc)."),
    Algorithm("E04", "DCT / IDCT", G_E, run_e04, source="C6 tr.44–49",
              note="Ảnh kết quả là log(1 + |hệ số DCT|) của từng khối 8×8."),
    Algorithm("E05", "Lượng tử hóa hệ số DCT", G_E, run_e05, [Q_SCALE], "C6 tr.50–52",
              note="DCT → lượng tử → giải lượng tử → IDCT."),
    Algorithm("E06", "Quét zig-zag", G_E, run_e06,
              [slider("keep", "Giữ N hệ số đầu theo zig-zag", 1, 64, 10)], "C6 tr.53, 55",
              note="Giữ N hệ số đầu của vector zig-zag, phần còn lại đặt 0, rồi dựng lại ảnh."),
    Algorithm("E07", "DPCM cho hệ số DC", G_E, run_e07, source="C6 tr.54, 56",
              note="Ảnh kết quả dựng từ DC đã giải mã DPCM (mỗi khối thành mức trung bình)."),
    Algorithm("E08", "RLE cho hệ số AC", G_E, run_e08, [Q_SCALE], "C6 tr.54, 57"),
    Algorithm("E09", "Quy trình JPEG đơn giản", G_E, run_e09, source="C6 tr.39–57"),

    Algorithm("F01", "Co (erosion)", G_F, _morph(morphology.erosion), MORPH_PARAMS, "C7 tr.9–17"),
    Algorithm("F02", "Giãn (dilation)", G_F, _morph(morphology.dilation), MORPH_PARAMS, "C7 tr.18–24"),
    Algorithm("F03", "Mở (opening)", G_F, _morph(morphology.opening), MORPH_PARAMS, "C7 tr.25–32"),
    Algorithm("F04", "Đóng (closing)", G_F, _morph(morphology.closing), MORPH_PARAMS, "C7 tr.33–37"),
    Algorithm("F05", "Làm đầy vùng (hole filling)", G_F, run_f05,
              [select("binarize", "Nhị phân hóa", BINARIZE),
               slider("T", "Ngưỡng tự chọn (khi không dùng Otsu)", 0, 255, 127),
               check("invert", "Đảo nhị phân (đối tượng là vùng tối)"),
               select("seed_mode", "Cách chọn seed", SEED_MODES),
               slider("seed_row", "Seed: hàng (%)", 0, 100, 50),
               slider("seed_col", "Seed: cột (%)", 0, 100, 50)],
              "C7 tr.40; DIP 4e §9.5", note="Phần tử cấu trúc chữ thập 3×3 như C7 tr.40."),

    Algorithm("H01", "Chuyển RGB ↔ CMY", G_H, run_h01, source="C4 tr.33–35", color=True,
              note="Ảnh kết quả là lượng mực CMY hiển thị như ảnh RGB."),
    Algorithm("H02", "Halftoning chọn mẫu (patterning)", G_H, run_h02,
              [select("cell", "Kích thước ô", (2, 4))], "C4 tr.49–53", max_size=128,
              note="Ảnh ra lớn gấp 2 hoặc 4 lần. Ma trận 4×4 trong code là Bayer, "
                   "khác ma trận Rylander ở C4 tr.51 (giữ nguyên code gốc)."),
    Algorithm("H03", "Ordered dithering", G_H, run_h03,
              [select("matrix", "Ma trận ngưỡng", tuple(H03_MATRICES))], "C4 tr.48, 54–55"),
    Algorithm("H04", "Khuếch tán lỗi 1D", G_H, run_h04, [CUTOFF], "C4 tr.56–60; câu 3.6, 3.7",
              note="Pixel bằng ngưỡng cho ra 255 (theo code gốc)."),
    Algorithm("H05", "Khuếch tán lỗi 2D Floyd–Steinberg", G_H, run_h05, [CUTOFF], "C4 tr.61–62"),
]

_BY_CODE = {algorithm.code: algorithm for algorithm in ALGORITHMS}


def get(code):
    return _BY_CODE[code]


def groups():
    seen = []
    for algorithm in ALGORITHMS:
        if algorithm.group not in seen:
            seen.append(algorithm.group)
    return seen


def execute(algorithm, image, params):
    """Chạy một thuật toán và kiểm tra đầu ra đúng format chung."""
    result = algorithm.run(np.ascontiguousarray(image), **params)
    output = np.asarray(result.image)
    if output.dtype != np.uint8 or output.ndim not in (2, 3):
        raise TypeError(f"{algorithm.code}: đầu ra phải là ảnh uint8, nhận {output.dtype} {output.shape}")
    result.info = {key: _fmt(value) for key, value in result.info.items()}
    return result
