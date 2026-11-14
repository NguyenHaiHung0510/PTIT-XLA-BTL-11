
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from B01 import mean_filter

image = np.array([
    [104, 100, 108],
    [99, 106, 98],
    [95, 90, 85]
], dtype=np.uint8)

print("Anh goc:")
print(image)

print("\nTrung binh pixel tam:")
print(image.sum() / 9)

print("\nAnh sau loc 3x3:")
print(mean_filter(image, 3))

path = Path(__file__).parent / "sample.jpg"

if path.exists():
    original = np.array(Image.open(path).convert("L"))
else:
    # Anh minh hoa co chi tiet va nhieu diem
    original = np.zeros((128, 128), dtype=np.uint8)
    original[25:100, 25:100] = 180
    original[45:80, 45:80] = 255

    rng = np.random.default_rng(42)
    noise = rng.normal(0, 30, original.shape)
    original = np.clip(
        original.astype(float) + noise, 0, 255
    ).astype(np.uint8)

filtered3 = mean_filter(original, 3)
filtered5 = mean_filter(original, 5)

fig, axes = plt.subplots(1, 3, figsize=(12, 4))

images = [original, filtered3, filtered5]
titles = [
    "Original",
    "Mean Filter 3x3",
    "Mean Filter 5x5"
]

for ax, img, title in zip(axes, images, titles):
    ax.imshow(img, cmap="gray", vmin=0, vmax=255)
    ax.set_title(title)
    ax.axis("off")

plt.tight_layout()
plt.show()
