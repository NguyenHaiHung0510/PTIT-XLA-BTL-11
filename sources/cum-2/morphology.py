"""Cụm 2, F01-F05 theo docs/bai-code.md; ảnh nhị phân 0/1.

Nguồn: C7 tr.9-17 (co), 18-24 (giãn), 25-32 (mở), 33-37 (đóng).
F05: đề C7 tr.40 và Digital Image Processing 4e, §9.5, Hole Filling,
Fig.9.17, Eq.(9-19), theo nguồn bổ sung mà bai-code.md chỉ định:
https://www.imageprocessingplace.com/downloads_V3/dip4e_downloads/dip4e_sample_book_material/dip4e_sample_chapters.pdf

Tự cài phép toán tập hợp; NumPy chỉ hỗ trợ mảng và phép toán logic.
Quy ước bản cài: mỗi bước trả cùng kích thước ảnh; ngoài khung là 0.
Chỉ các phần tử 1 của SE tham gia, 0 của SE không đòi ảnh phải bằng 0.
anchor=(hàng,cột) xác định gốc SE; không đồng nghĩa với trọng tâm hình.
Mặc định lấy tâm SE lẻ; SE chẵn phải truyền anchor rõ ràng. Cho phép gốc
ở ngoài ma trận SE để biểu diễn phần tử có gốc lệch như C7 tr.14-15.
Chạy test từ gốc repo: python src/cum-2/test_morphology.py
"""

import numpy as np


CROSS_3 = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=np.uint8)


def _binary(array, name):
    array = np.asarray(array)
    if (array.ndim != 2 or array.size == 0 or array.dtype.kind not in 'biuf'
            or not np.isin(array, [0, 1]).all()):
        raise ValueError(f'{name} phải là ma trận nhị phân 2D không rỗng, chỉ chứa 0/1.')
    return array.astype(bool)


def _structure(se, anchor):
    se = _binary(se, 'SE')
    if not np.any(se):
        raise ValueError('SE cần ít nhất một phần tử 1.')
    if anchor is None:
        if any(length % 2 == 0 for length in se.shape):
            raise ValueError('SE chẵn cần chỉ rõ anchor=(hàng,cột).')
        anchor = (se.shape[0] // 2, se.shape[1] // 2)
    if (not isinstance(anchor, (tuple, list, np.ndarray)) or len(anchor) != 2
            or any(not isinstance(v, (int, np.integer)) for v in anchor)):
        raise ValueError('anchor phải gồm hai số nguyên (hàng,cột).')
    offsets = [(int(r) - int(anchor[0]), int(c) - int(anchor[1]))
               for r, c in np.argwhere(se)]
    return offsets


def _sample(image, dr, dc):
    """out[r,c]=image[r+dr,c+dc]; phần ngoài ảnh là 0, không cuộn vòng."""
    h, w = image.shape
    out = np.zeros_like(image, dtype=bool)
    r0, r1 = max(0, -dr), min(h, h - dr)
    c0, c1 = max(0, -dc), min(w, w - dc)
    if r0 < r1 and c0 < c1:
        out[r0:r1, c0:c1] = image[r0 + dr:r1 + dr, c0 + dc:c1 + dc]
    return out


def _erode(image, offsets):
    result = np.ones_like(image, dtype=bool)
    for dr, dc in offsets:
        result &= _sample(image, dr, dc)
    return result


def _dilate(image, offsets):
    result = np.zeros_like(image, dtype=bool)
    for dr, dc in offsets:
        # Phép cộng tập hợp: mỗi điểm ảnh a tạo điểm a+b với b thuộc SE.
        # Tương đương kiểm tra B phản xạ có hits ảnh tại pixel đang xét.
        result |= _sample(image, -dr, -dc)
    return result


def erosion(image, se, anchor=None):
    """F01, C7 tr.9-17: g[z]=1 khi mọi z+b (b thuộc SE) đều thuộc ảnh.

    Giữ nguyên tọa độ SE khi kiểm tra fit; trả uint8 0/1.
    """
    image = _binary(image, 'Ảnh')
    offsets = _structure(se, anchor)
    return _erode(image, offsets).astype(np.uint8)


def dilation(image, se, anchor=None):
    """F02, C7 tr.18-24: A⊕B={a+b}; trả uint8 0/1.

    Với SE không đối xứng, phép giãn kiểm tra hits của SE phản xạ:
    g[z]=OR f[z-b]. Không dùng cùng dấu offset với phép co.
    Với SE đối xứng quanh gốc (như ví dụ phổ biến trong C7), B phản xạ=B.
    """
    image = _binary(image, 'Ảnh')
    offsets = _structure(se, anchor)
    return _dilate(image, offsets).astype(np.uint8)


def opening(image, se, anchor=None):
    """F03, C7 tr.25-32, công thức tr.26: (A⊖B)⊕B.

    Co rồi giãn; giữ nguyên SE và gốc ở cả hai bước.
    """
    image = _binary(image, 'Ảnh')
    offsets = _structure(se, anchor)
    return _dilate(_erode(image, offsets), offsets).astype(np.uint8)


def closing(image, se, anchor=None):
    """F04, C7 tr.33-37: (A⊕B)⊖B, giãn rồi co.

    Theo quy ước giữ cùng khung và padding 0 của bản cài, phần giãn ra
    ngoài khung bị cắt trước bước co. Vì vậy vật thể sát mép có thể bị mất
    pixel ở mép, không áp dụng tính bao hàm A⊆closing(A) tại đó.
    """
    image = _binary(image, 'Ảnh')
    offsets = _structure(se, anchor)
    return _erode(_dilate(image, offsets), offsets).astype(np.uint8)


def hole_filling(image, se, seeds, anchor=None, return_steps=False):
    """F05, C7 tr.40; DIP4e §9.5, Eq.(9-19): làm đầy các lỗ đã chọn.

    seeds là danh sách điểm (hàng,cột), mỗi lỗ cần ít nhất một điểm.
    X0 chỉ có 1 ở seeds; Xk=(Xk-1⊕B)∩A^c; dừng khi Xk=Xk-1.
    Kết quả: filled=A∪Xcuối; holes=Xcuối; iterations là số lần X thay đổi.
    return_steps=True trả thêm steps=[X0,...,Xcuối], không lặp bản ổn định.

    Người gọi phải chọn seed trong lỗ, không phải nền ngoài: thuật toán
    phát triển mọi thành phần nền được seed trỏ tới, không tự tìm seed.
    SE phải chứa gốc để X tăng đơn điệu và hội tụ. Dùng CROSS_3 cho SE
    ở C7 tr.40 (liên thông nền 4); không tự đổi thành SE vuông 3x3.
    """
    image = _binary(image, 'Ảnh')
    offsets = _structure(se, anchor)
    if (0, 0) not in offsets:
        raise ValueError('SE làm đầy vùng phải chứa gốc (phần tử 1 tại anchor).')
    try:
        seeds = list(seeds)
    except TypeError as error:
        raise ValueError('seeds phải là danh sách điểm (hàng,cột).') from error
    if not seeds:
        raise ValueError('Cần ít nhất một seed trong lỗ muốn làm đầy.')
    marker = np.zeros_like(image, dtype=bool)
    for point in seeds:
        if (not isinstance(point, (tuple, list, np.ndarray)) or len(point) != 2
                or any(not isinstance(v, (int, np.integer)) for v in point)):
            raise ValueError('Mỗi seed phải gồm hai số nguyên (hàng,cột).')
        r, c = point
        if not (0 <= r < image.shape[0] and 0 <= c < image.shape[1]):
            raise ValueError('Seed phải nằm trong ảnh.')
        if image[r, c]:
            raise ValueError('Seed phải ở nền 0 trong lỗ, không nằm trên đối tượng 1.')
        marker[r, c] = True
    complement = ~image
    steps = [marker.astype(np.uint8)] if return_steps else None
    iterations = 0
    while True:
        updated = _dilate(marker, offsets) & complement
        if np.array_equal(updated, marker):
            break
        marker = updated
        iterations += 1
        if return_steps:
            steps.append(marker.astype(np.uint8))
    result = {'filled': (image | marker).astype(np.uint8),
              'holes': marker.astype(np.uint8), 'iterations': iterations}
    if return_steps:
        result['steps'] = steps
    return result
