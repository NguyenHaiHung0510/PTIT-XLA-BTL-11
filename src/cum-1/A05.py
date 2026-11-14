
import numpy as np


def gamma_transform(image, gamma=1.0):
    """
    A05 - Bien doi luy thua Gamma.
    Nguon: c3.pdf, trang 18-20.

    Input:
        image: Ma tran anh xam 0-255
        gamma: He so gamma > 0

    Output:
        Ma tran anh xam uint8.
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

    if not isinstance(gamma, (int, float, np.number)):
        raise ValueError("Gamma phai la so")

    if not np.isfinite(gamma) or gamma <= 0:
        raise ValueError("Gamma phai > 0 va huu han")

    # Chuan hoa ve [0, 1]
    normalized = img.astype(np.float64) / 255.0

    # Tu thuc hien cong thuc Gamma
    result = 255.0 * np.power(normalized, gamma)

    # Gioi han va lam tron .5 len
    result = np.floor(np.clip(result, 0, 255) + 0.5)

    return result.astype(np.uint8)
