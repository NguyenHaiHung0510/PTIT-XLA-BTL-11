
import numpy as np


def equalize_histogram(image, levels=256):
    """
    A08 - Can bang histogram.
    Nguon: c3.pdf, trang 32-38.

    Input:
        image: Anh xam 2 chieu
        levels: So muc xam L

    Output:
        result: Anh sau can bang
        histogram: Histogram ban dau
        cdf: Xac suat tich luy
        mapping: Bang anh xa muc xam
    """
    img = np.asarray(image)

    if not isinstance(levels, (int, np.integer)) or levels < 2:
        raise ValueError("levels phai la so nguyen >= 2")

    if img.ndim != 2 or img.size == 0:
        raise ValueError("Anh phai la ma tran 2 chieu khong rong")

    if not np.issubdtype(img.dtype, np.integer):
        raise ValueError("Pixel phai la so nguyen")

    if np.any(img < 0) or np.any(img >= levels):
        raise ValueError("Pixel ngoai mien muc xam")

    # Buoc 1: Tinh histogram
    histogram = np.zeros(levels, dtype=np.int64)

    for pixel in img.flat:
        histogram[int(pixel)] += 1

    # Buoc 2: Xac suat moi muc xam
    probability = histogram / img.size

    # Buoc 3: Xac suat tich luy
    cdf = np.zeros(levels, dtype=np.float64)
    total = 0.0

    for i in range(levels):
        total += probability[i]
        cdf[i] = total

    # Buoc 4: Bang anh xa
    mapping = np.floor((levels - 1) * cdf + 0.5)
    mapping = np.clip(mapping, 0, levels - 1).astype(np.int64)

    # Buoc 5: Tao anh moi
    result = mapping[img]

    return result, histogram, cdf, mapping
