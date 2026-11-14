
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from B03 import k_nearest_mean_filter

# Vi du trong slide C3 trang 51-52
image = np.array([
    [1, 2, 3, 2],
    [4, 16, 2, 1],
    [4, 2, 1, 1],
    [2, 1, 2, 1]
], dtype=np.uint8)

result = k_nearest_mean_filter(
    image, k=3, theta=2, kernel_size=3
)

print("Anh goc:")
print(image)

print("\nAnh sau loc:")
print(result)

print("\nPixel tam (1,1):")
print("Truoc:", image[1, 1])
print("Sau:", result[1, 1])

# Demo anh thuc te
path = Path(__file__).parent / "sample.jpg"

if path.exists():
    original = np.array(Image.open(path).convert("L"))
else:
    original = np.full((128, 128), 60, dtype=np.uint8)
    original[25:100, 25:100] = 180
    original[45:80, 45:80] = 230

    rng = np.random.default_rng(42)

    # Them nhieu xung de minh hoa
    mask = rng.random(original.shape)

    original[mask < 0.05] = 0
    original[mask > 0.95] = 255

filtered = k_nearest_mean_filter(
    original, k=3, theta=2, kernel_size=3
)

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

axes[0].imshow(original, cmap="gray", vmin=0, vmax=255)
axes[0].set_title("Original")

axes[1].imshow(filtered, cmap="gray", vmin=0, vmax=255)
axes[1].set_title("K-Nearest Mean k=3, theta=2")

for ax in axes:
    ax.axis("off")

plt.tight_layout()
plt.show()
