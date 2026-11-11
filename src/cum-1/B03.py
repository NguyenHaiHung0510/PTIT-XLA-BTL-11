
import numpy as np


def k_nearest_mean_filter(image, k=3, theta=2, kernel_size=3):
    """
    B03 - Loc trung binh k gia tri gan nhat co nguong.
    Nguon: c3.pdf, trang 50-52.

    Input:
        image: Anh xam 2 chieu (0-255)
        k: So gia tri duoc chon, bao gom pixel tam
        theta: Nguong so sanh
        kernel_size: Kich thuoc cua so le

    Output:
        Anh sau loc, uint8.

    Quy uoc:
        Padding = 0
        Hoa khoang cach: uu tien muc xam lon hon
        Lam tron 0.5 len
    """
    img = np.asarray(image)

    if img.ndim != 2 or img.size == 0:
        raise ValueError("Anh phai la ma tran 2 chieu khong rong")

    if not np.issubdtype(img.dtype, np.number):
        raise ValueError("Pixel phai la so")

    if not np.isfinite(img).all():
        raise ValueError("Pixel phai huu han")

    if np.any(img < 0) or np.any(img > 255):
        raise ValueError("Pixel phai nam trong [0, 255]")

    if (
        not isinstance(kernel_size, (int, np.integer))
        or isinstance(kernel_size, (bool, np.bool_))
        or kernel_size < 3
        or kernel_size % 2 == 0
    ):
        raise ValueError("kernel_size phai le va >= 3")

    if (
        not isinstance(k, (int, np.integer))
        or isinstance(k, (bool, np.bool_))
        or k < 1
        or k > kernel_size ** 2
    ):
        raise ValueError("k phai nam trong [1, kernel_size^2]")

    if (
        not isinstance(theta, (int, float, np.number))
        or not np.isfinite(theta)
        or theta < 0
    ):
        raise ValueError("theta phai la so huu han >= 0")

    img = img.astype(np.float64)

    h, w = img.shape
    pad = kernel_size // 2

    padded = np.pad(
        img, pad, mode="constant", constant_values=0
    )

    result = np.zeros((h, w), dtype=np.float64)

    for i in range(h):
        for j in range(w):
            center = img[i, j]

            window = padded[
                i:i + kernel_size,
                j:j + kernel_size
            ].flatten()

            # Sap xep theo khoang cach tang dan.
            # Neu bang khoang cach, muc xam lon hon dung truoc.
            candidates = sorted(
                window,
                key=lambda v: (abs(v - center), -v)
            )

            selected = candidates[:k]
            average = sum(selected) / k

            if abs(center - average) > theta:
                result[i, j] = average
            else:
                result[i, j] = center

    result = np.floor(np.clip(result, 0, 255) + 0.5)

    return result.astype(np.uint8)
