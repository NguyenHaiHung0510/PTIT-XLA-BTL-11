
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from B02 import (
    weighted_mean_filter,
    gaussian_filter,
    WEIGHTED_3X3,
    GAUSSIAN_5X5
)

# Demo ma tran
image = np.array([
    [10, 20, 30, 40, 50],
    [20, 40, 60, 80, 100],
    [30, 60, 200, 120, 150],
    [40, 80, 120, 160, 200],
    [50, 100, 150, 200, 250]
], dtype=np.uint8)

print("Anh goc:")
print(image)

print("\nKernel trong so 3x3:")
print(WEIGHTED_3X3)

print("\nKernel Gaussian 5x5:")
print(GAUSSIAN_5X5)

print("\nSau loc trong so:")
print(weighted_mean_filter(image))

print("\nSau loc Gaussian:")
print(gaussian_filter(image))

# Demo anh thuc te
path = Path(__file__).parent / "sample.jpg"

if path.exists():
    original = np.array(Image.open(path).convert("L"))
else:
    original = np.zeros((128, 128), dtype=np.uint8)
    original[25:100, 25:100] = 180
    original[45:80, 45:80] = 255

    rng = np.random.default_rng(42)
    noise = rng.normal(0, 30, original.shape)

    original = np.clip(
        original.astype(float) + noise, 0, 255
    ).astype(np.uint8)

weighted = weighted_mean_filter(original)
gaussian = gaussian_filter(original)

fig, axes = plt.subplots(1, 3, figsize=(13, 4))

images = [original, weighted, gaussian]
titles = [
    "Original",
    "Weighted Mean 3x3",
    "Gaussian Approx 5x5"
]

for ax, img, title in zip(axes, images, titles):
    ax.imshow(img, cmap="gray", vmin=0, vmax=255)
    ax.set_title(title)
    ax.axis("off")

plt.tight_layout()
plt.show()
