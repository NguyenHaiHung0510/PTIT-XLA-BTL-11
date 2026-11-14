
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from A06 import contrast_stretch

r1, s1, r2, s2 = 80, 30, 160, 220

image = np.array([
    [0, 40, 80],
    [100, 120, 160],
    [180, 200, 255]
], dtype=np.uint8)

print("Anh goc:")
print(image)

print("\nAnh sau keo gian tuong phan:")
print(contrast_stretch(image, r1, s1, r2, s2))

path = Path(__file__).parent / "sample.jpg"

if path.exists():
    original = np.array(Image.open(path).convert("L"))
else:
    original = np.tile(
        np.arange(256, dtype=np.uint8),
        (150, 1)
    )

output = contrast_stretch(
    original, r1, s1, r2, s2
)

fig, axes = plt.subplots(1, 3, figsize=(14, 4))

axes[0].imshow(original, cmap="gray", vmin=0, vmax=255)
axes[0].set_title("Original")
axes[0].axis("off")

axes[1].imshow(output, cmap="gray", vmin=0, vmax=255)
axes[1].set_title("Contrast Stretching")
axes[1].axis("off")

x = np.arange(256, dtype=np.uint8).reshape(1, 256)
y = contrast_stretch(x, r1, s1, r2, s2)[0]

axes[2].plot(x[0], y)
axes[2].plot(
    [0, r1, r2, 255],
    [0, s1, s2, 255],
    "o"
)
axes[2].set_title("Transformation Curve")
axes[2].set_xlabel("Input")
axes[2].set_ylabel("Output")
axes[2].set_xlim(0, 255)
axes[2].set_ylim(0, 255)
axes[2].grid(True)

plt.tight_layout()
plt.show()
