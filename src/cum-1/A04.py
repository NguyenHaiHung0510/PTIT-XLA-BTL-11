
import numpy as np


def validate_image(image):
    img = np.asarray(image)

    if img.ndim != 2:
        raise ValueError("Anh phai la ma tran 2 chieu")

    if not np.issubdtype(img.dtype, np.number):
        raise ValueError("Pixel phai la so")

    if not np.isfinite(img).all():
        raise ValueError("Pixel phai huu han")

    if np.any(img < 0) or np.any(img > 255):
        raise ValueError("Pixel phai nam trong [0, 255]")

    return img.astype(np.float64)


def to_uint8(image):
    # Lam tron 0.5 len va gioi han [0, 255]
    return np.floor(
        np.clip(image, 0, 255) + 0.5
    ).astype(np.uint8)


def log_transform(image):
    """
    A04 - Bien doi logarithm.
    c3.pdf, trang 15-17.
    """
    img = validate_image(image)

    c = 255 / np.log1p(255)
    result = c * np.log1p(img)

    return to_uint8(result)


def inverse_log_transform(image):
    """
    A04 - Bien doi inverse logarithm.
    Dung ham nguoc cua log da chuan hoa.
    """
    img = validate_image(image)

    c = 255 / np.log1p(255)
    result = np.expm1(img / c)

    return to_uint8(result)
