
import numpy as np


def validate_image(image, levels=256):
    img = np.asarray(image)

    if not isinstance(levels, (int, np.integer)):
        raise ValueError("levels phai la so nguyen")

    if levels < 2:
        raise ValueError("levels phai >= 2")

    if img.ndim != 2:
        raise ValueError("Anh phai la ma tran 2 chieu")

    if not np.issubdtype(img.dtype, np.integer):
        raise ValueError("Pixel phai la so nguyen")

    if np.any(img < 0) or np.any(img >= levels):
        raise ValueError("Pixel ngoai mien muc xam")

    return img


def histogram(image, levels=256):
    """
    A07 - Tinh histogram.
    Nguon: c3.pdf, trang 23-31.
    """
    img = validate_image(image, levels)

    counts = np.zeros(levels, dtype=np.int64)

    # Tu dem so pixel tai tung muc xam
    for pixel in img.flat:
        counts[int(pixel)] += 1

    return counts


def histogram_probability(image, levels=256):
    img = validate_image(image, levels)

    if img.size == 0:
        raise ValueError("Anh khong duoc rong")

    return histogram(img, levels) / img.size


def transform_histogram(image, mapping, levels=256):
    """
    Tinh histogram sau bien doi g' = f(g).

    mapping: ham nhan mot muc xam va tra muc xam moi.

    Output:
        transformed: Anh sau bien doi
        new_hist: Histogram cua anh moi
    """
    img = validate_image(image, levels)

    # Tao bang anh xa cho cac muc xam
    lookup = np.zeros(levels, dtype=np.int64)

    for g in range(levels):
        new_g = mapping(g)

        if (
            not isinstance(new_g, (int, np.integer))
            or not 0 <= new_g < levels
        ):
            raise ValueError("Muc xam sau bien doi khong hop le")

        lookup[g] = new_g

    transformed = lookup[img]
    new_hist = histogram(transformed, levels)

    return transformed, new_hist
