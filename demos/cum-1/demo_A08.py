
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from A08 import equalize_histogram

image = np.array([
    [3, 1, 4, 4, 2, 3],
    [3, 2, 2, 0, 5, 1],
    [1, 2, 3, 1, 0, 1],
    [4, 1, 0, 2, 4, 4],
    [3, 1, 0, 1, 0, 1],
    [2, 1, 3, 2, 1, 3]
])

levels = 6

result, hist, cdf, mapping = equalize_histogram(
    image, levels
)

hist_after = np.zeros(levels, dtype=int)
for pixel in result.flat:
    hist_after[int(pixel)] += 1

print("Anh goc:\n", image)
print("\nHistogram goc:", hist)
print("CDF:", np.round(cdf, 4))
print("Bang anh xa:", mapping)
print("\nAnh sau can bang:\n", result)
print("Histogram sau can bang:", hist_after)

fig, axes = plt.subplots(2, 2, figsize=(10, 8))

axes[0, 0].imshow(
    image, cmap="gray", vmin=0, vmax=5
)
axes[0, 0].set_title("Original")
axes[0, 0].axis("off")

axes[0, 1].imshow(
    result, cmap="gray", vmin=0, vmax=5
)
axes[0, 1].set_title("Equalized")
axes[0, 1].axis("off")

axes[1, 0].bar(range(levels), hist)
axes[1, 0].set_title("Histogram Before")
axes[1, 0].set_xticks(range(levels))

axes[1, 1].bar(range(levels), hist_after)
axes[1, 1].set_title("Histogram After")
axes[1, 1].set_xticks(range(levels))

plt.tight_layout()
plt.show()
