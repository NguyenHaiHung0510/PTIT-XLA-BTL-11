
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "cum-1"))

from A01 import negative

# Demo ma tran
image = np.array([
    [0, 50, 100],
    [150, 200, 255],
    [10, 20, 30]
], dtype=np.uint8)

result = negative(image)

print("Anh goc:\n", image)
print("Anh am ban:\n", result)

# Demo anh thuc te neu co, neu khong dung gradient
path = Path(__file__).parent / "sample.jpg"

if path.exists():
    original = np.array(Image.open(path).convert("L"))
else:
    original = np.tile(
        np.arange(256, dtype=np.uint8),
        (150, 1)
    )

output = negative(original)

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

axes[0].imshow(original, cmap="gray", vmin=0, vmax=255)
axes[0].set_title("Input - Original")

axes[1].imshow(output, cmap="gray", vmin=0, vmax=255)
axes[1].set_title("Output - Negative")

for ax in axes:
    ax.axis("off")

plt.tight_layout()
plt.show()
