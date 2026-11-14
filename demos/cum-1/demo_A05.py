
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from A05 import gamma_transform

image = np.array([
    [0, 50, 100],
    [150, 200, 255],
    [10, 20, 30]
], dtype=np.uint8)

print("Anh goc:")
print(image)

print("\nGamma = 0.5:")
print(gamma_transform(image, 0.5))

print("\nGamma = 2:")
print(gamma_transform(image, 2.0))

path = Path(__file__).parent / "sample.jpg"

if path.exists():
    original = np.array(Image.open(path).convert("L"))
else:
    original = np.tile(
        np.arange(256, dtype=np.uint8),
        (150, 1)
    )

bright = gamma_transform(original, 0.5)
dark = gamma_transform(original, 2.0)

fig, axes = plt.subplots(1, 3, figsize=(13, 4))

images = [original, bright, dark]
titles = [
    "Original",
    "Gamma = 0.5 (Brighter)",
    "Gamma = 2.0 (Darker)"
]

for ax, img, title in zip(axes, images, titles):
    ax.imshow(img, cmap="gray", vmin=0, vmax=255)
    ax.set_title(title)
    ax.axis("off")

plt.tight_layout()
plt.show()
