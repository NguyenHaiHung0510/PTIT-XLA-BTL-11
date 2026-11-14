
import numpy as np


WEIGHTED_3X3 = np.array([
    [1, 2, 1],
    [2, 4, 2],
    [1, 2, 1]
], dtype=np.float64) / 16


GAUSSIAN_5X5 = np.array([
    [2, 4, 5, 4, 2],
    [4, 9, 12, 9, 4],
    [5, 12, 15, 12, 5],
    [4, 9, 12, 9, 4],
    [2, 4, 5, 4, 2]
], dtype=np.float64) / 159


def weighted_filter(image, kernel):
    """
    B02 - Loc trung binh co trong so.

    Input:
        image: Anh xam 2 chieu (0-255)
        kernel: Ma tran trong so

    Output:
        Anh sau loc, uint8.

    Padding: 0
    Lam tron: 0.5 len
    """
    img = np.asarray(image)

    if img.ndim != 2 or img.size == 0:
        raise ValueError("Anh phai la ma tran 2 chieu khong rong")

    if not np.issubdtype(img.dtype, np.number):
        raise ValueError("Pixel phai la so")

    if not np.isfinite(img).all():
        raise ValueError("Pixel phai huu han")

    if np.any(img < 0) or np.any(img > 255):
        raise ValueError("Pixel ngoai mien [0, 255]")

    kernel = np.asarray(kernel)

    if kernel.ndim != 2:
        raise ValueError("Kernel phai la ma tran 2 chieu")

    kh, kw = kernel.shape

    if kh < 1 or kw < 1 or kh % 2 == 0 or kw % 2 == 0:
        raise ValueError("Kich thuoc kernel phai le")

    if not np.issubdtype(kernel.dtype, np.number):
        raise ValueError("Trong so phai la so")

    if not np.isfinite(kernel).all():
        raise ValueError("Kernel phai huu han")

    if np.any(kernel < 0):
        raise ValueError("Trong so phai khong am")

    total_weight = float(np.sum(kernel))

    if total_weight <= 0:
        raise ValueError("Tong trong so phai > 0")

    # Chuan hoa tong trong so ve 1
    weights = kernel.astype(np.float64) / total_weight
    img = img.astype(np.float64)

    h, w = img.shape
    ph, pw = kh // 2, kw // 2

    padded = np.pad(
        img, ((ph, ph), (pw, pw)),
        mode="constant", constant_values=0
    )

    result = np.zeros((h, w), dtype=np.float64)

    # Tu cai dat phep loc, khong goi ham filter san
    for i in range(h):
        for j in range(w):
            total = 0.0

            for a in range(kh):
                for b in range(kw):
                    total += (
                        padded[i + a, j + b]
                        * weights[a, b]
                    )

            result[i, j] = total

    result = np.floor(np.clip(result, 0, 255) + 0.5)

    return result.astype(np.uint8)


def weighted_mean_filter(image):
    """Kernel 3x3 - C3 trang 49."""
    return weighted_filter(image, WEIGHTED_3X3)


def gaussian_filter(image):
    """Kernel Gaussian xap xi 5x5 - C5 trang 40."""
    return weighted_filter(image, GAUSSIAN_5X5)
