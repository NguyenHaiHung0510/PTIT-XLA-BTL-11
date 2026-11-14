
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from A04 import log_transform, inverse_log_transform

image = np.array([
    [0, 15, 50],
    [100, 150, 200],
    [220, 240, 255]
], dtype=np.uint8)

print("Anh goc:")
print(image)

print("\nBien doi Log:")
print(log_transform(image))

print("\nBien doi Inverse Log:")
print(inverse_log_transform(image))

path = Path(__file__).parent / "sample.jpg"

if path.exists():
    original = np.array(Image.open(path).convert("L"))
else:
    original = np.tile(
        np.arange(256, dtype=np.uint8),
        (150, 1)
    )

log_image = log_transform(original)
inverse_image = inverse_log_transform(original)

fig, axes = plt.subplots(1, 3, figsize=(13, 4))

images = [original, log_image, inverse_image]
titles = ["Original", "Log Transform", "Inverse Log"]

for ax, img, title in zip(axes, images, titles):
    ax.imshow(img, cmap="gray", vmin=0, vmax=255)
    ax.set_title(title)
    ax.axis("off")

plt.tight_layout()
plt.show()
