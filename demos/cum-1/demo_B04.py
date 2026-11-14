
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from B04 import median_filter

image = np.array([
    [10, 11, 12],
    [10, 255, 12],
    [11, 12, 13]
], dtype=np.uint8)

result = median_filter(image, 3)

print("Anh goc:")
print(image)

print("\nAnh sau loc:")
print(result)

print("\nPixel tam truoc:", image[1, 1])
print("Pixel tam sau:", result[1, 1])

path = Path(__file__).parent / "sample.jpg"

if path.exists():
    original = np.array(Image.open(path).convert("L"))
else:
    original = np.full((128, 128), 60, dtype=np.uint8)
    original[25:100, 25:100] = 180
    original[45:80, 45:80] = 230

    rng = np.random.default_rng(42)
    mask = rng.random(original.shape)

    original[mask < 0.05] = 0
    original[mask > 0.95] = 255

filtered3 = median_filter(original, 3)
filtered5 = median_filter(original, 5)

fig, axes = plt.subplots(1, 3, figsize=(13, 4))

images = [original, filtered3, filtered5]
titles = [
    "Original - Salt & Pepper Noise",
    "Median Filter 3x3",
    "Median Filter 5x5"
]

for ax, img, title in zip(axes, images, titles):
    ax.imshow(img, cmap="gray", vmin=0, vmax=255)
    ax.set_title(title)
    ax.axis("off")

plt.tight_layout()
plt.show()
