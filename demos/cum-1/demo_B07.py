
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from B07 import midpoint_filter

image = np.array([
    [100, 110, 120],
    [90, 150, 130],
    [80, 140, 160]
], dtype=np.uint8)

result = midpoint_filter(image, 3)

print("Anh goc:")
print(image)

print("\nAnh sau loc Midpoint:")
print(result)

print("\nPixel tam truoc:", image[1, 1])
print("Pixel tam sau:", result[1, 1])

# Demo anh co nhieu Gaussian
path = Path(__file__).parent / "sample.jpg"

if path.exists():
    original = np.array(Image.open(path).convert("L"))
else:
    original = np.full((128, 128), 100, dtype=np.uint8)
    original[25:100, 25:100] = 170
    original[45:80, 45:80] = 210

    rng = np.random.default_rng(42)
    noise = rng.normal(0, 25, original.shape)

    original = np.clip(
        original.astype(float) + noise, 0, 255
    ).astype(np.uint8)

filtered3 = midpoint_filter(original, 3)
filtered5 = midpoint_filter(original, 5)

fig, axes = plt.subplots(1, 3, figsize=(13, 4))

images = [original, filtered3, filtered5]
titles = [
    "Original - Gaussian Noise",
    "Midpoint Filter 3x3",
    "Midpoint Filter 5x5"
]

for ax, img, title in zip(axes, images, titles):
    ax.imshow(img, cmap="gray", vmin=0, vmax=255)
    ax.set_title(title)
    ax.axis("off")

plt.tight_layout()
plt.show()
