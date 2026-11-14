
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from A02 import adjust_brightness

# Demo ma tran
image = np.array([
    [0, 50, 100],
    [150, 200, 255],
    [10, 20, 30]
], dtype=np.uint8)

print("Anh goc:")
print(image)

print("\nTang sang (c=1.5):")
print(adjust_brightness(image, 1.5))

print("\nGiam sang (c=0.5):")
print(adjust_brightness(image, 0.5))

# Anh mau de visualize
path = Path(__file__).parent / "sample.jpg"

if path.exists():
    original = np.array(Image.open(path).convert("L"))
else:
    x = np.arange(256, dtype=np.uint8)
    original = np.tile(x, (150, 1))

brighter = adjust_brightness(original, 1.5)
darker = adjust_brightness(original, 0.5)

fig, axes = plt.subplots(1, 3, figsize=(12, 4))

images = [original, brighter, darker]
titles = [
    "Original",
    "Brighter (c=1.5)",
    "Darker (c=0.5)"
]

for ax, img, title in zip(axes, images, titles):
    ax.imshow(img, cmap="gray", vmin=0, vmax=255)
    ax.set_title(title)
    ax.axis("off")

plt.tight_layout()
plt.show()
