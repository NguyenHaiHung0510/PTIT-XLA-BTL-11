
import numpy as np


def threshold(image, T=127, max_value=1):
    """
    A03 - Phan nguong co dinh.
    Nguon: c3.pdf, trang PDF 14.

    Input:
        image: Anh xam 2 chieu, muc xam 0-255
        T: Nguong phan tach
        max_value: Gia tri pixel sang (1 hoac 255)

    Output:
        Ma tran anh sau phan nguong.
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

    if not isinstance(T, (int, float, np.number)):
        raise ValueError("Nguong T phai la so")

    if not np.isfinite(T) or T < 0 or T > 255:
        raise ValueError("T phai nam trong [0, 255]")

    if max_value not in (1, 255):
        raise ValueError("max_value phai la 1 hoac 255")

    # Tu cai dat phep so sanh nguong
    result = np.where(img > T, max_value, 0)

    return result.astype(np.uint8)
