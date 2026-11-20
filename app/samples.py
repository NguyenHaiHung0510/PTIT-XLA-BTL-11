"""Ảnh mẫu tự sinh để demo khi chưa có ảnh tải lên."""

import numpy as np

SAMPLES = (
    "Hình khối",
    "Hình khối + nhiễu muối tiêu",
    "Hình khối + nhiễu Gaussian",
    "Dải gradient",
)


def _shapes(size):
    yy, xx = np.mgrid[0:size, 0:size] / size
    base = 60 + 40 * xx  # nền tối, sáng dần sang phải
    rect = (yy > 0.12) & (yy < 0.45) & (xx > 0.10) & (xx < 0.40)
    circle = (yy - 0.70) ** 2 + (xx - 0.28) ** 2 < 0.17 ** 2
    radius = (yy - 0.35) ** 2 + (xx - 0.70) ** 2
    ring = (radius < 0.20 ** 2) & (radius > 0.10 ** 2)  # vòng có lỗ ở giữa (cho F05)
    bar = (yy > 0.78) & (yy < 0.90) & (xx > 0.55) & (xx < 0.92)
    return base, {"rect": rect, "circle": circle, "ring": ring, "bar": bar}


def make_sample(name, size=256, color=False):
    rng = np.random.default_rng(11)
    if name == "Dải gradient":
        ramp = np.tile(np.linspace(0, 255, size), (size, 1))
        gray = ramp
        rgb = np.stack([ramp, ramp[::-1, ::-1], np.full_like(ramp, 128)], axis=-1)
    else:
        base, masks = _shapes(size)
        gray = base.copy()
        for key, value in (("rect", 200), ("circle", 230), ("ring", 175), ("bar", 140)):
            gray[masks[key]] = value
        rgb = np.stack([base * 0.7, base * 0.85, base * 1.1], axis=-1)
        for key, value in (("rect", (220, 60, 50)), ("circle", (60, 170, 80)),
                           ("ring", (240, 200, 40)), ("bar", (70, 90, 220))):
            rgb[masks[key]] = value
    image = rgb if color else gray
    if name.endswith("muối tiêu"):
        noise = rng.random(image.shape[:2])
        image = image.copy()
        image[noise < 0.04] = 0
        image[noise > 0.96] = 255
    elif name.endswith("Gaussian"):
        image = image + rng.normal(0, 18, image.shape)
    return np.clip(np.floor(image + 0.5), 0, 255).astype(np.uint8)
