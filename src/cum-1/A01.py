
import numpy as np


def negative(image, max_value=255):
    """
    A01 - Phep bien doi am ban.
    Nguon: c3.pdf, trang 13.

    Input: Ma tran anh xam 2 chieu.
    Output: Ma tran anh sau bien doi am ban.
    """

    img = np.asarray(image)

    if img.ndim != 2:
        raise ValueError("Anh phai la ma tran 2 chieu")

    if not np.issubdtype(img.dtype, np.number):
        raise ValueError("Pixel phai la gia tri so")

    if not np.isfinite(img).all():
        raise ValueError("Pixel phai la so huu han")

    if not np.isfinite(max_value) or max_value <= 0:
        raise ValueError("Muc xam toi da khong hop le")

    if np.any(img < 0) or np.any(img > max_value):
        raise ValueError("Pixel nam ngoai mien muc xam")

    result = max_value - img.astype(np.float64)

    if max_value == 255 and np.issubdtype(img.dtype, np.integer):
        return result.astype(np.uint8)

    return result
