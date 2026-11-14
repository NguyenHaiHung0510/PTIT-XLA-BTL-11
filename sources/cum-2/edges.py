"""Cụm 2, C01-C07: tự cài theo C5 và docs/bai-code.md.

Padding 0, trượt nguyên chiều mặt nạ, tính trung gian bằng float64.
Mỗi hàm ghi rõ trang PDF tương ứng; không dùng bộ lọc thư viện có sẵn.
"""

from collections import deque

import numpy as np


# C5 tr.16: x tăng theo hàng, y tăng theo cột trong công thức sai phân.
DIFF_X = np.array([[-1], [1]], dtype=float)
DIFF_Y = np.array([[-1, 1]], dtype=float)
# C5 tr.17.
ROBERTS_X = np.array([[1, 0], [0, -1]], dtype=float)
ROBERTS_Y = np.array([[0, -1], [1, 0]], dtype=float)
# C5 tr.19: giữ nguyên tên Mx, My và dấu của mặt nạ trên slide.
PREWITT_X = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=float)
PREWITT_Y = PREWITT_X.T.copy()
SOBEL_X = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)
SOBEL_Y = SOBEL_X.T.copy()
# C5 tr.29,35: tâm âm; không lấy trị tuyệt đối trước khi làm sắc nét.
LAPLACIAN_4 = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=float)
LAPLACIAN_8 = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype=float)
# C5 tr.40: xấp xỉ Gaussian 5x5, tổng hệ số = 159.
GAUSSIAN_5 = np.array([
    [2, 4, 5, 4, 2],
    [4, 9, 12, 9, 4],
    [5, 12, 15, 12, 5],
    [4, 9, 12, 9, 4],
    [2, 4, 5, 4, 2],
], dtype=float) / 159.0


def gray_array(image):
    """Nhận ma trận xám 2D không rỗng, hữu hạn; tính bằng float64."""
    image = np.asarray(image, dtype=np.float64)
    if image.ndim != 2 or image.size == 0:
        raise ValueError('Ảnh phải là ma trận xám 2D không rỗng.')
    if not np.isfinite(image).all():
        raise ValueError('Ảnh không được chứa NaN hoặc vô cực.')
    return image


def correlate(image, kernel, anchor=None):
    """Trượt mặt nạ nguyên chiều, padding 0, kết quả cùng cỡ ảnh.

    anchor là (hàng, cột) của mặt nạ đặt lên pixel đang xét.
    Mặc định lấy tâm; mặt nạ chẵn phải truyền anchor rõ ràng.
    """
    image = gray_array(image)
    kernel = gray_array(kernel)
    kh, kw = kernel.shape
    if anchor is None:
        if kh % 2 == 0 or kw % 2 == 0:
            raise ValueError('Mặt nạ chẵn cần chỉ rõ anchor.')
        anchor = (kh // 2, kw // 2)
    ar, ac = anchor
    if not (0 <= ar < kh and 0 <= ac < kw):
        raise ValueError('anchor phải nằm trong mặt nạ.')
    padded = np.pad(image, ((ar, kh - 1 - ar), (ac, kw - 1 - ac)))
    result = np.zeros_like(image)
    # Chỉ dùng NumPy cho phép toán mảng; tự trượt từng hệ số mặt nạ.
    h, w = image.shape
    for r in range(kh):
        for c in range(kw):
            result += kernel[r, c] * padded[r:r + h, c:c + w]
    return result


def gradient_result(gx, gy, magnitude='l1', threshold=None):
    """Trả thành phần có dấu, độ lớn, góc (độ), và ảnh biên nếu có T.

    l1: |Gx|+|Gy| (tr.20); l2: sqrt(Gx²+Gy²) (tr.14,24).
    sum: Gx+Gy, dành cho yêu cầu cộng ma trận trong đề tự luận.
    """
    if magnitude == 'l1':
        strength = np.abs(gx) + np.abs(gy)
    elif magnitude == 'l2':
        strength = np.sqrt(gx * gx + gy * gy)
    elif magnitude == 'sum':
        strength = gx + gy
    else:
        raise ValueError('magnitude phải là l1, l2 hoặc sum.')
    result = {
        'gx': gx, 'gy': gy, 'magnitude': strength,
        # atan2 xử lý được Gx=0; (0,0) quy ước góc 0 độ.
        'angle': np.degrees(np.arctan2(gy, gx)),
    }
    if threshold is not None:
        if not np.isfinite(threshold) or threshold < 0:
            raise ValueError('Ngưỡng phải hữu hạn và không âm.')
        result['edges'] = (strength > threshold).astype(np.uint8) * 255
    return result


def gradient_1d(image, magnitude='l1', threshold=None):
    """C01, C5 tr.14-16: f(x+1,y)-f(x,y), f(x,y+1)-f(x,y)."""
    gx = correlate(image, DIFF_X, anchor=(0, 0))
    gy = correlate(image, DIFF_Y, anchor=(0, 0))
    return gradient_result(gx, gy, magnitude, threshold)


def roberts(image, magnitude='l1', threshold=None):
    """C02, C5 tr.17: neo tại góc trên trái của cửa sổ 2x2."""
    gx = correlate(image, ROBERTS_X, anchor=(0, 0))
    gy = correlate(image, ROBERTS_Y, anchor=(0, 0))
    return gradient_result(gx, gy, magnitude, threshold)


def prewitt(image, magnitude='l1', threshold=None):
    """C03, C5 tr.18-22: mặt nạ tr.19, không chia hệ số ngầm."""
    return gradient_result(correlate(image, PREWITT_X),
                           correlate(image, PREWITT_Y), magnitude, threshold)


def sobel(image, magnitude='l1', threshold=None):
    """C04, C5 tr.18-19,23-26: mặt nạ tr.19."""
    return gradient_result(correlate(image, SOBEL_X),
                           correlate(image, SOBEL_Y), magnitude, threshold)


def laplacian(image, neighbors=4):
    """C05, C5 tr.28-30,35: trả đáp ứng có dấu, tâm -4 hoặc -8."""
    if neighbors not in (4, 8):
        raise ValueError('neighbors phải là 4 hoặc 8.')
    kernel = LAPLACIAN_4 if neighbors == 4 else LAPLACIAN_8
    return correlate(image, kernel)


def sharpen_laplacian(image, neighbors=4):
    """C06, C5 tr.31-35: g=f-Laplacian(f); giữ kết quả thô có dấu."""
    image = gray_array(image)
    return image - laplacian(image, neighbors)


def quantize_directions(angle):
    """C07, C5 tr.42-43: làm tròn góc về 0,45,90,135 độ."""
    angle = gray_array(angle) % 180
    return (((angle + 22.5) // 45).astype(np.uint8) % 4) * 45


def non_maximum_suppression(magnitude, directions):
    """C07, C5 tr.44-45: chỉ giữ điểm lớn hơn cả hai lân cận.

    Góc đo với trục ngang hướng phải, trục đứng hướng lên (tr.41).
    Lân cận ngoài ảnh có độ lớn 0 theo quy ước padding của repo.
    """
    magnitude = gray_array(magnitude)
    directions = gray_array(directions)
    if magnitude.shape != directions.shape:
        raise ValueError('Độ lớn và hướng phải cùng kích thước.')
    if not np.isin(directions, [0, 45, 90, 135]).all():
        raise ValueError('Hướng phải là 0,45,90 hoặc 135 độ.')
    padded = np.pad(magnitude, 1)
    output = np.zeros_like(magnitude)
    # Cặp lân cận đúng theo tr.45: Đ-T, ĐB-TN, B-N, TB-ĐN.
    offsets = {0: (0, 1), 45: (-1, 1), 90: (-1, 0), 135: (-1, -1)}
    for r in range(magnitude.shape[0]):
        for c in range(magnitude.shape[1]):
            dr, dc = offsets[int(directions[r, c])]
            center = padded[r + 1, c + 1]
            before = padded[r + 1 + dr, c + 1 + dc]
            after = padded[r + 1 - dr, c + 1 - dc]
            if center > before and center > after:
                output[r, c] = center
    return output


def hysteresis(suppressed, low, high):
    """C07, C5 tr.47-48: nối chuỗi điểm yếu tới điểm mạnh bằng 8 lân cận.

    Mạnh: > high; yếu: [low, high] và khác 0. Giá trị 0 đã bị NMS
    loại luôn bỏ, kể cả low=0. Không nối với điểm yếu cô lập.
    """
    suppressed = gray_array(suppressed)
    if not (np.isfinite(low) and np.isfinite(high) and 0 <= low < high):
        raise ValueError('Cần 0 <= low < high và hai ngưỡng hữu hạn.')
    strong = suppressed > high
    candidates = (suppressed >= low) & (suppressed > 0)
    linked = strong.copy()
    queue = deque(map(tuple, np.argwhere(strong)))
    h, w = suppressed.shape
    while queue:
        r, c = queue.popleft()
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r + dr, c + dc
                if (0 <= nr < h and 0 <= nc < w
                        and candidates[nr, nc] and not linked[nr, nc]):
                    linked[nr, nc] = True
                    queue.append((nr, nc))
    return linked.astype(np.uint8) * 255


def canny(image, low, high):
    """C07, C5 tr.36-49: Gaussian -> Sobel -> NMS -> hysteresis.

    Giữ lại mọi bước để đối chiếu slide. Ngưỡng trên độ lớn thô L1,
    không chuẩn hóa về 0..255 trước khi phân ngưỡng.
    """
    smoothed = correlate(image, GAUSSIAN_5)
    gx = correlate(smoothed, SOBEL_X)
    # Tr.41 dùng Gy có hàng trên dương, trái dấu My của tr.19.
    gy = correlate(smoothed, -SOBEL_Y)
    result = gradient_result(gx, gy)
    directions = quantize_directions(result['angle'])
    suppressed = non_maximum_suppression(result['magnitude'], directions)
    result.update(smoothed=smoothed, directions=directions,
                  suppressed=suppressed, edges=hysteresis(suppressed, low, high))
    return result