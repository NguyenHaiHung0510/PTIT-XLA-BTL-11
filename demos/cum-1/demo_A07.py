
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from A07 import histogram, transform_histogram

image = np.array([
    [1, 2, 1, 3, 2, 1],
    [4, 4, 3, 2, 4, 0],
    [6, 9, 2, 3, 2, 1],
    [6, 2, 0, 5, 3, 0],
    [3, 4, 0, 5, 1, 5],
    [5, 6, 8, 9, 3, 6]
])

levels = 10

# Cau 3.1: f(g) = |g - 4|
image1, hist1 = transform_histogram(
    image, lambda g: abs(g - 4), levels
)

# Cau 3.2: f(g) = |2g - 9|
image2, hist2 = transform_histogram(
    image, lambda g: abs(2 * g - 9), levels
)

hist_original = histogram(image, levels)

print("Histogram goc:", hist_original)
print("Histogram f(g)=|g-4|:", hist1)
print("Histogram f(g)=|2g-9|:", hist2)

fig, axes = plt.subplots(2, 3, figsize=(13, 8))

images = [image, image1, image2]
hists = [hist_original, hist1, hist2]

titles = [
    "Original",
    "f(g) = |g - 4|",
    "f(g) = |2g - 9|"
]

for i in range(3):
    axes[0, i].imshow(
        images[i], cmap="gray", vmin=0, vmax=9
    )
    axes[0, i].set_title(titles[i])
    axes[0, i].axis("off")

    axes[1, i].bar(range(levels), hists[i])
    axes[1, i].set_title("Histogram")
    axes[1, i].set_xlabel("Gray level")
    axes[1, i].set_ylabel("Frequency")
    axes[1, i].set_xticks(range(levels))

plt.tight_layout()
plt.show()
