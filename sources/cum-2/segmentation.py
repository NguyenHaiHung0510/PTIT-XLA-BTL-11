"""Cụm 2, D01-D09 theo docs/bai-code.md và C5 tr.62-100.

NumPy chỉ hỗ trợ mảng/phép toán; tự cài logic, không gọi bộ phân vùng sẵn.
Các hàm D01-D05 nhận histogram h[b] (tần số hoặc trọng số không âm).
D06-D09 nhận ảnh xám 2D; kết quả vùng dùng mask hoặc ma trận nhãn.
Chạy kiểm tra từ gốc repo: python src/cum-2/test_segmentation.py

Quy ước được chọn khi slide chưa ấn định:
- Padding histogram bằng 0; không làm tròn trung gian.
- Đỉnh histogram hòa nhau: lấy mức xám nhỏ nhất. Otsu hòa cực đại thì
  lấy TRUNG BÌNH các ngưỡng, đúng yêu cầu riêng ở tr.67.
- Phân vị là mức đầu tiên có CDF >= p%; không nội suy mức xám.
- Vùng kề nhau theo 4 lân cận chung cạnh; riêng phát triển vùng cho phép
  chọn 4 hoặc 8. Thứ tự xét ổn định, không tự đặt tiêu chuẩn đồng nhất.
"""

from collections import deque
from dataclasses import dataclass

import numpy as np


def _image(image):
    image = np.asarray(image, dtype=np.float64)
    if image.ndim != 2 or image.size == 0 or not np.isfinite(image).all():
        raise ValueError('Cần ảnh xám 2D không rỗng, mọi giá trị hữu hạn.')
    return image


def _histogram(hist, require_mass=True):
    hist = np.asarray(hist, dtype=np.float64)
    if (hist.ndim != 1 or hist.size == 0 or not np.isfinite(hist).all()
            or np.any(hist < 0)):
        raise ValueError('Histogram phải là dãy 1D không rỗng, hữu hạn, không âm.')
    if require_mass and not np.any(hist > 0):
        raise ValueError('Histogram cần ít nhất một mức có trọng số dương.')
    return hist


def histogram(image, levels=256):
    """Hỗ trợ D01-D05: tự đếm mức xám nguyên 0..levels-1, không lượng tử ngầm."""
    image = _image(image)
    if not isinstance(levels, (int, np.integer)) or levels <= 0:
        raise ValueError('levels phải là số nguyên dương.')
    if np.any(image < 0) or np.any(image >= levels) or np.any(image != np.floor(image)):
        raise ValueError('Ảnh phải có mức xám nguyên trong 0..levels-1.')
    result = np.zeros(levels, dtype=np.int64)
    for value in image.flat:
        result[int(value)] += 1
    return result


def smooth_histogram(hist, window=3):
    """D01, C5 tr.62: hsmooth[b] = tổng hraw[b-w] / W.

    W dương lẻ (slide gợi ý 3 hoặc 5); padding 0 theo repo.
    Chia đúng W kể cả ở biên, không chuẩn hóa lại tổng histogram.
    """
    hist = _histogram(hist, require_mass=False)
    if not isinstance(window, (int, np.integer)) or window <= 0 or window % 2 == 0:
        raise ValueError('window phải là số nguyên dương lẻ.')
    radius = window // 2
    padded = np.pad(hist, (radius, radius))
    result = np.zeros_like(hist)
    for offset in range(window):
        result += padded[offset:offset + len(hist)]
    return result / window


def otsu_threshold(hist):
    """D02, C5 tr.65-70, công thức tr.67; trả ngưỡng và bảng phương sai.

    Hai lớp: mức <= k và > k. Các k có lớp rỗng không xét (NaN trong bảng).
    Hòa cực đại: trung bình mọi k cực đại; so sánh số thực bằng isclose
    với rtol=1e-12, atol=0 để tránh lệch do sai số cộng dồn.
    Histogram chỉ có một mức: trả chính mức đó; không tồn tại phân đôi.
    """
    hist = _histogram(hist)
    # Chia trước theo max giúp tránh tràn tổng khi histogram có trọng số lớn.
    probabilities = hist / hist.max()
    probabilities /= probabilities.sum()
    levels = np.arange(len(hist), dtype=float)
    cumulative = np.cumsum(probabilities)
    means = np.cumsum(levels * probabilities)
    global_mean = means[-1]
    variance = np.full(len(hist), np.nan)
    support = np.flatnonzero(hist)
    if len(support) == 1:
        return {'threshold': float(support[0]), 'between_variance': variance,
                'maxima': np.array([], dtype=int)}
    # Chặn theo support để không xem sai số CDF ~1 là lớp có trọng số dương.
    candidates = np.arange(int(support[0]), int(support[-1]))
    p1 = cumulative[candidates]
    # Tính trọng số phía phải trực tiếp để tránh phép trừ 1-P1 gần 0.
    p2 = np.cumsum(probabilities[::-1])[::-1][candidates + 1]
    variance[candidates] = (global_mean * p1 - means[candidates]) ** 2 / (p1 * p2)
    maximum = np.max(variance[candidates])
    maxima = candidates[np.isclose(variance[candidates], maximum, rtol=1e-12, atol=0)]
    return {'threshold': float(maxima.mean()), 'between_variance': variance,
            'maxima': maxima}


def isodata_threshold(hist, initial=None, delta=1e-6, max_iterations=1000):
    """D03, C5 tr.71-75: Tk+1=(mu1+mu2)/2; dừng khi |Tk+1-Tk|<delta.

    initial mặc định là mức xám trung bình, theo tr.71. Giữ ngưỡng thực:
    với mức xám nguyên, phân lớp <=T tương đương <=floor(T).
    Trả threshold, history (gồm T0), means (mu1,mu2 của từng lần cập nhật).
    Không âm thầm làm tròn hay trả kết quả chưa hội tụ.

    Lưu ý nguồn: bảng p(z) làm tròn ở tr.74 với T0=3 cho T1=2.572222...,
    T2=2.103125, T3=2.103125 khi áp đúng tr.71-72; không tái tạo các số
    2.574/2.438 in trong lời giải. Phân lớp cuối vẫn có floor(T)=2.
    """
    hist = _histogram(hist)
    if not np.isfinite(delta) or delta <= 0:
        raise ValueError('delta phải hữu hạn và dương.')
    if not isinstance(max_iterations, (int, np.integer)) or max_iterations <= 0:
        raise ValueError('max_iterations phải là số nguyên dương.')
    weights = hist / hist.max()
    levels = np.arange(len(hist), dtype=float)
    threshold = float(np.dot(levels, weights) / weights.sum()) if initial is None else float(initial)
    if not np.isfinite(threshold):
        raise ValueError('initial phải hữu hạn.')
    history = [threshold]
    means = []
    support = np.flatnonzero(hist)
    if len(support) == 1:
        value = float(support[0])
        return {'threshold': value, 'history': history + [value], 'means': means}
    for _ in range(max_iterations):
        left = levels <= threshold
        w1, w2 = weights[left].sum(), weights[~left].sum()
        if w1 == 0 or w2 == 0:
            raise ValueError('Ngưỡng tạo lớp rỗng; cần chọn lại initial.')
        mu1 = float(np.dot(levels[left], weights[left]) / w1)
        mu2 = float(np.dot(levels[~left], weights[~left]) / w2)
        updated = (mu1 + mu2) / 2
        means.append((mu1, mu2))
        history.append(updated)
        if abs(updated - threshold) < delta:
            return {'threshold': updated, 'history': history, 'means': means}
        threshold = updated
    raise RuntimeError('Isodata chưa hội tụ trong max_iterations.')


def background_symmetry_threshold(hist, percentile):
    """D04, C5 tr.76-77,79: nền sáng, đối tượng bên trái đỉnh như tr.77.

    maxp là đỉnh; a là phân vị của CDF TOÀN histogram: P(a)>=p%.
    Trả threshold=2*maxp-a, peak và percentile_level. percentile truyền
    theo phần trăm (vd 95 hoặc 88). Kiểm tra a ở phía phải đỉnh (a>=maxp).
    Không tự đổi phía, không dùng p% chiều cao đỉnh hay CDF riêng nửa nền.
    Ngưỡng phản chiếu không bị cắt về 0..L-1 để giữ công thức slide.
    """
    hist = _histogram(hist)
    if not np.isfinite(percentile) or not 0 < percentile <= 100:
        raise ValueError('percentile phải nằm trong (0,100].')
    weights = hist / hist.max()
    cdf = np.cumsum(weights) / weights.sum()
    peak = int(np.argmax(hist))
    reached = np.flatnonzero((cdf >= percentile / 100) |
                             np.isclose(cdf, percentile / 100, rtol=0, atol=1e-14))
    level = int(reached[0])
    if level < peak:
        raise ValueError('Phân vị ở trái đỉnh; không thỏa cách tìm phía phải của tr.77.')
    return {'threshold': 2 * peak - level, 'peak': peak, 'percentile_level': level}


def triangle_threshold(hist, minimum=None):
    """D05, C5 tr.78: đoạn nối (bmin,h[bmin]) và (bmax,h[bmax]).

    bmax là mức có histogram cao nhất. bmin mặc định là mức nhỏ nhất
    có pixel (phân vị 0%); có thể truyền minimum theo miền mức xám của đề.
    Chỉ xét phía trái đỉnh theo slide; không tự chọn/đảo sang đuôi phải.
    Trả threshold, minimum, peak và distances (NaN ngoài đoạn xét).
    Hòa khoảng cách: lấy mức nhỏ nhất. Nếu bmin=bmax, không có tam giác,
    báo lỗi thay vì tự đưa ngưỡng không có ý nghĩa.
    """
    hist = _histogram(hist)
    peak = int(np.argmax(hist))
    if minimum is None:
        minimum = int(np.flatnonzero(hist)[0])
    if not isinstance(minimum, (int, np.integer)) or not 0 <= minimum < peak:
        raise ValueError('Cần 0<=minimum<peak để tạo tam giác bên trái đỉnh (tr.78).')
    # Co giãn đồng nhất cả hai trục giữ nguyên điểm xa nhất, tránh tràn.
    scale = max(float(hist.max()), float(len(hist)))
    x0, y0 = minimum / scale, hist[minimum] / scale
    dx, dy = (peak - minimum) / scale, (hist[peak] - hist[minimum]) / scale
    distances = np.full(len(hist), np.nan)
    for b in range(minimum, peak + 1):
        distances[b] = abs(dx * (hist[b] / scale - y0) - dy * (b / scale - x0)) / np.hypot(dx, dy)
    segment = distances[minimum:peak + 1]
    maximum = segment.max()
    maxima = np.flatnonzero(np.isclose(segment, maximum, rtol=1e-12, atol=0))
    # Trả khoảng cách theo tọa độ gốc của histogram, không đổi thang đầu vào.
    distances *= scale
    return {'threshold': int(minimum + maxima[0]), 'minimum': int(minimum),
            'peak': peak, 'distances': distances}


def _neighbors(r, c, shape, connectivity=4):
    offsets = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    if connectivity == 8:
        offsets += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in offsets:
        nr, nc = r + dr, c + dc
        if 0 <= nr < shape[0] and 0 <= nc < shape[1]:
            yield nr, nc


def _decision(value):
    if not isinstance(value, (bool, np.bool_)):
        raise ValueError('Tiêu chuẩn phải trả một giá trị bool.')
    return bool(value)


def region_growing(image, seed, similar, connectivity=4):
    """D06, C5 tr.85-86: mở rộng từ seed, so với seed cố định (tr.85).

    similar(candidate_value, seed_value) là tiêu chuẩn do người gọi cung cấp;
    không so với trung bình vùng đang đổi. Kết quả là mask bool cùng cỡ ảnh.
    Tham số connectivity=4 là quy ước bản cài, có thể chọn 8.
    """
    image = _image(image)
    if connectivity not in (4, 8):
        raise ValueError('connectivity phải là 4 hoặc 8.')
    if (len(seed) != 2 or any(not isinstance(v, (int, np.integer)) for v in seed)
            or not 0 <= seed[0] < image.shape[0] or not 0 <= seed[1] < image.shape[1]):
        raise ValueError('seed phải là (hàng,cột) nguyên nằm trong ảnh.')
    if not callable(similar):
        raise ValueError('Cần hàm similar(candidate_value, seed_value).')
    seed = tuple(seed)
    seed_value = float(image[seed])
    selected = np.zeros(image.shape, dtype=bool)
    visited = np.zeros(image.shape, dtype=bool)
    selected[seed] = visited[seed] = True
    queue = deque([seed])
    while queue:
        r, c = queue.popleft()
        for nr, nc in _neighbors(r, c, image.shape, connectivity):
            if not visited[nr, nc]:
                visited[nr, nc] = True
                if _decision(similar(float(image[nr, nc]), seed_value)):
                    selected[nr, nc] = True
                    queue.append((nr, nc))
    return selected


def _labels(labels, shape=None):
    labels = np.asarray(labels)
    if (labels.ndim != 2 or labels.size == 0 or labels.dtype.kind not in 'iu'
            or np.any(labels < 0) or (shape is not None and labels.shape != shape)):
        raise ValueError('Nhãn phải là ma trận số nguyên không âm, cùng cỡ ảnh.')
    return labels.copy()


def region_adjacency(labels):
    """Hỗ trợ D07/D09, tr.88,96: RAG với kề chung cạnh, không tính chạm góc."""
    labels = _labels(labels)
    graph = {int(label): set() for label in np.unique(labels)}
    for r in range(labels.shape[0]):
        for c in range(labels.shape[1]):
            a = int(labels[r, c])
            for nr, nc in ((r + 1, c), (r, c + 1)):
                if nr < labels.shape[0] and nc < labels.shape[1]:
                    b = int(labels[nr, nc])
                    if a != b:
                        graph[a].add(b)
                        graph[b].add(a)
    return graph


def _validate_regions(image, labels, predicate):
    if not callable(predicate):
        raise ValueError('Cần hàm predicate(values) kiểm tra P(R).')
    for label in np.unique(labels):
        mask = labels == label
        if not _decision(predicate(image[mask])):
            raise ValueError('Mỗi vùng khởi tạo phải thỏa P(R), theo tr.87.')
        start = tuple(np.argwhere(mask)[0])
        visited = {start}
        queue = deque([start])
        while queue:
            r, c = queue.popleft()
            for point in _neighbors(r, c, image.shape):
                if mask[point] and point not in visited:
                    visited.add(point)
                    queue.append(point)
        if len(visited) != int(mask.sum()):
            raise ValueError('Mỗi nhãn phải biểu diễn một vùng liên thông 4.')


def region_merging(image, labels, predicate):
    """D07, C5 tr.87-88: nhận các vùng khởi tạo, xây RAG, hợp đến ổn định.

    predicate(values) kiểm tra P(R) trên TOÀN BỘ giá trị trong vùng/hợp vùng,
    không tự thay bằng khoảng cách hai trung bình. Mỗi vùng đầu vào phải
    liên thông 4 và thỏa P(R). Khi có nhiều cặp hợp được, xét nhãn tăng dần;
    hợp cặp đầu tiên rồi cập nhật RAG, lặp tới khi không còn cặp hợp được.
    Kết quả nhãn được đánh lại 0..n-1. Không sửa mảng nhãn của người gọi.
    """
    image = _image(image)
    labels = _labels(labels, image.shape)
    _validate_regions(image, labels, predicate)
    while True:
        graph = region_adjacency(labels)
        pair = None
        for a in sorted(graph):
            for b in sorted(graph[a]):
                if b > a and _decision(predicate(image[(labels == a) | (labels == b)])):
                    pair = (a, b)
                    break
            if pair is not None:
                break
        if pair is None:
            break
        a, b = pair
        labels[labels == b] = a
    # searchsorted chỉ ánh xạ lại tập nhãn tăng dần về các số liên tiếp.
    return np.searchsorted(np.unique(labels), labels)


@dataclass
class QuadNode:
    """Node quadtree tr.91-92; children theo thứ tự TL,TR,BL,BR."""
    row: int
    col: int
    size: int
    children: tuple = ()


def quadtree_split(image, predicate):
    """D08, C5 tr.89-93: tách 4 khi P(R)=False.

    Đúng giả định tr.91: ảnh NxN, N là lũy thừa của 2; không padding hay
    tự đổi kích thước. predicate(values) do người gọi định nghĩa.
    Trả {'labels': ma trận nhãn lá, 'tree': QuadNode gốc}.
    Nếu cả vùng 1 pixel không thỏa P thì không thể phân vùng, báo lỗi.
    """
    image = _image(image)
    size = image.shape[0]
    if image.shape[1] != size or size & (size - 1):
        raise ValueError('Quadtree cần ảnh NxN, N là lũy thừa 2 (C5 tr.91).')
    if not callable(predicate):
        raise ValueError('Cần hàm predicate(values) kiểm tra P(R).')
    labels = np.full(image.shape, -1, dtype=np.int64)
    next_label = 0

    def split(row, col, length):
        nonlocal next_label
        node = QuadNode(row, col, length)
        values = image[row:row + length, col:col + length].reshape(-1)
        if _decision(predicate(values)):
            labels[row:row + length, col:col + length] = next_label
            next_label += 1
        elif length == 1:
            raise ValueError('Vùng 1 pixel không thỏa P; không thể tách tiếp.')
        else:
            half = length // 2
            node.children = tuple(split(r, c, half) for r, c in [
                (row, col), (row, col + half),
                (row + half, col), (row + half, col + half)])
        return node

    tree = split(0, 0, size)
    return {'labels': labels, 'tree': tree}


def split_and_merge(image, predicate):
    """D09, C5 tr.94-100: tách vùng sai P rồi hợp các vùng kề có hợp thỏa P.

    Tách đệ quy đến khi mọi lá thỏa P, sau đó lặp hợp tới ổn định.
    Vì mỗi phép hợp chỉ nhận hợp vùng thỏa P, không tạo vùng cần tách lại.
    Kết quả thỏa: mọi vùng đồng nhất và không còn cặp kề hợp được (tr.95).
    Trả labels cuối, split_labels và tree của PHA TÁCH để đối chiếu;
    cây pha tách không biểu diễn các vùng đã hợp có hình dạng bất kỳ.
    """
    split = quadtree_split(image, predicate)
    labels = region_merging(image, split['labels'], predicate)
    return {'labels': labels, 'split_labels': split['labels'], 'tree': split['tree']}
