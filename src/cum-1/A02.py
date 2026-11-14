
import numpy as np


def adjust_brightness(image, c=1.0):
    """
    A02 - Bien doi tuyen tinh do sang.
    Nguon: c3.pdf trang 18, gamma = 1.

    Input:
        image: Anh xam 2 chieu (0-255)
        c: He so do sang, c >= 0

    Output:
        Anh xam sau bien doi, uint8.

    Cong thuc: s = c * r
    """

    img = np.asarray(image)

    if img.ndim != 2:
        raise ValueError("Anh phai la ma tran 2 chieu")

    if not np.issubdtype(img.dtype, np.number):
        raise ValueError("Pixel phai la gia tri so")

    if not np.isfinite(img).all():
        raise ValueError("Pixel phai la so huu han")

    if np.any(img < 0) or np.any(img > 255):
        raise ValueError("Pixel phai nam trong [0, 255]")

    if not np.isscalar(c) or not isinstance(
        c, (int, float, np.number)
    ):
        raise ValueError("He so c phai la so")

    if not np.isfinite(c) or c < 0:
        raise ValueError("He so c phai >= 0 va huu han")

    # Thuc hien bien doi tuyen tinh
    result = img.astype(np.float64) * c

    # Gioi han gia tri va lam tron .5 len
    result = np.clip(result, 0, 255)
    result = np.floor(result + 0.5)

    return result.astype(np.uint8)
