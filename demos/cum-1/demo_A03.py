
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from A03 import threshold

T = 127

# Demo ma tran
image = np.array([
    [0, 50, 100],
    [127, 128, 255],
    [10, 200, 150]
], dtype=np.uint8)

result = threshold(image, T)

print("Anh goc:")
print(image)

print("\nAnh sau phan nguong (0/1):")
print(result)

# Demo anh thuc te
path = Path(__file__).parent / "sample.jpg"

if path.exists():
    original = np.array(Image.open(path).convert("L"))
else:
    original = np.tile(
        np.arange(256, dtype=np.uint8),
        (150, 1)
    )

output = threshold(original, T, max_value=255)

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

axes[0].imshow(
    original, cmap="gray", vmin=0, vmax=255
)
axes[0].set_title("Input - Original")

axes[1].imshow(
    output, cmap="gray", vmin=0, vmax=255
)
axes[1].set_title(f"Output - Threshold T={T}")

for ax in axes:
    ax.axis("off")

plt.tight_layout()
plt.show()
