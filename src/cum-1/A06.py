
import numpy as np


def contrast_stretch(image, r1=80, s1=30, r2=160, s2=220):
    """
    A06 - Keo gian tuong phan theo doan.
    Nguon: c3.pdf, trang 21.

    Input: Anh xam 0-255, hai diem dieu khien.
    Output: Anh xam sau bien doi (uint8).
    """
    img = np.asarray(image)

    if img.ndim != 2:
        raise ValueError("Anh phai la ma tran 2 chieu")

    if not np.issubdtype(img.dtype, np.number):
        raise ValueError("Pixel phai la so")

    if not np.isfinite(img).all():
        raise ValueError("Pixel phai huu han")

    if np.any(img < 0) or np.any(img > 255):
        raise ValueError("Pixel phai nam trong [0, 255]")

    values = (r1, s1, r2, s2)

    if not all(
        isinstance(v, (int, float, np.number))
        and np.isfinite(v)
        for v in values
    ):
        raise ValueError("Cac moc phai la so huu han")

    if not (0 < r1 < r2 < 255):
        raise ValueError("Can 0 < r1 < r2 < 255")

    if not (0 <= s1 <= s2 <= 255):
        raise ValueError("Can 0 <= s1 <= s2 <= 255")

    img = img.astype(np.float64)
    result = np.zeros_like(img)

    mask1 = img <= r1
    mask2 = (img > r1) & (img <= r2)
    mask3 = img > r2

    result[mask1] = (s1 / r1) * img[mask1]

    result[mask2] = s1 + (
        (s2 - s1) / (r2 - r1)
    ) * (img[mask2] - r1)

    result[mask3] = s2 + (
        (255 - s2) / (255 - r2)
    ) * (img[mask3] - r2)

    result = np.floor(np.clip(result, 0, 255) + 0.5)

    return result.astype(np.uint8)
