"""Giao diện demo: chọn thuật toán → đưa ảnh vào → chạy → xem ảnh kết quả.

Chạy từ gốc repo:  streamlit run app/main.py
"""

import hashlib
import io
import math
import time

import numpy as np
import streamlit as st
from PIL import Image

import algorithms as alg
import samples

st.set_page_config(page_title="Demo Xử lý ảnh – Nhóm 11", layout="wide")


def render_param(param, prefix):
    key = f"{prefix}:{param.key}"
    if param.kind == "slider":
        return st.slider(param.label, param.min, param.max, param.default, param.step,
                         key=key, help=param.help)
    if param.kind == "select":
        return st.selectbox(param.label, param.options, index=param.options.index(param.default),
                            key=key, help=param.help)
    return st.checkbox(param.label, param.default, key=key, help=param.help)


def for_display(image, min_side=256):
    """Phóng to ảnh nhỏ bằng lân cận gần nhất để dễ nhìn (không đổi dữ liệu kết quả)."""
    height, width = image.shape[:2]
    factor = math.ceil(min_side / max(height, width))
    if factor <= 1:
        return image
    return np.repeat(np.repeat(image, factor, axis=0), factor, axis=1)


def png_bytes(image):
    buffer = io.BytesIO()
    Image.fromarray(image).save(buffer, format="PNG")
    return buffer.getvalue()


st.title("Demo thuật toán Xử lý ảnh – Nhóm 11")
st.caption("Chọn thuật toán ở thanh bên → chọn ảnh → nhấn **Chạy thuật toán** → xem ảnh kết quả.")

with st.sidebar:
    st.header("1. Thuật toán")
    group = st.selectbox("Nhóm", alg.groups())
    choices = [a for a in alg.ALGORITHMS if a.group == group]
    algorithm = st.selectbox("Thuật toán", choices, format_func=lambda a: f"{a.code} – {a.name}")
    st.caption(f"Nguồn: {algorithm.source}")
    if algorithm.note:
        st.info(algorithm.note)

    st.header("2. Tham số")
    params = {p.key: render_param(p, algorithm.code) for p in algorithm.params}
    if not algorithm.params:
        st.write("Thuật toán không có tham số.")

    st.header("3. Ảnh đầu vào")
    source = st.radio("Nguồn ảnh", ("Ảnh mẫu", "Tải ảnh lên"), horizontal=True)
    upload, sample_name = None, None
    if source == "Tải ảnh lên":
        upload = st.file_uploader("Chọn ảnh", type=["png", "jpg", "jpeg", "bmp", "tif", "tiff", "webp"])
    else:
        sample_name = st.selectbox("Ảnh mẫu", samples.SAMPLES)
    max_side = st.slider("Cạnh dài tối đa khi xử lý (px)", 64, 512, 256, 32,
                         help="Các thuật toán viết bằng vòng lặp Python nên ảnh lớn sẽ chạy chậm.")
    run_clicked = st.button("▶ Chạy thuật toán", type="primary")

limit = min(max_side, algorithm.max_size or max_side)
if source == "Tải ảnh lên":
    if upload is None:
        st.info("Hãy tải một ảnh lên ở thanh bên, hoặc chọn **Ảnh mẫu**.")
        st.stop()
    image = np.asarray(Image.open(upload).convert("RGB" if algorithm.color else "L"))
else:
    image = samples.make_sample(sample_name, limit, color=algorithm.color)
image = alg.fit_max_side(image, limit)

signature = (algorithm.code, tuple(sorted(params.items())),
             hashlib.md5(image.tobytes()).hexdigest(), image.shape)

if run_clicked:
    with st.spinner(f"Đang chạy {algorithm.code} – {algorithm.name}..."):
        started = time.perf_counter()
        try:
            outcome = (alg.execute(algorithm, image, params), None)
        except Exception as error:  # hiển thị lỗi đầu vào thay vì làm sập giao diện
            outcome = (None, f"{type(error).__name__}: {error}")
        st.session_state["last"] = (signature, outcome, time.perf_counter() - started)

kind = "RGB" if image.ndim == 3 else "xám"
left, right = st.columns(2)
left.subheader("Ảnh đầu vào")
left.image(for_display(image), caption=f"{image.shape[1]}×{image.shape[0]}, ảnh {kind}")
right.subheader("Ảnh kết quả")

last = st.session_state.get("last")
if not last or last[0] != signature:
    right.info("Nhấn **▶ Chạy thuật toán** để xem kết quả.")
    st.stop()

_, (result, error), elapsed = last
if error:
    right.error(f"Không chạy được {algorithm.code}: {error}")
    st.stop()

out = result.image
right.image(for_display(out), caption=f"{algorithm.code} – {out.shape[1]}×{out.shape[0]}")
right.download_button("Tải ảnh kết quả (PNG)", png_bytes(out),
                      file_name=f"{algorithm.code}_ket_qua.png", mime="image/png")
st.success(f"Chạy xong {algorithm.code} trong {elapsed:.2f} giây.")

if result.info:
    st.subheader("Thông tin")
    st.table({"Đại lượng": list(result.info), "Giá trị": [str(v) for v in result.info.values()]})

if result.extras:
    st.subheader("Ảnh trung gian / bổ sung")
    columns = st.columns(min(3, len(result.extras)))
    for index, (caption, extra) in enumerate(result.extras):
        columns[index % len(columns)].image(for_display(extra), caption=caption)
