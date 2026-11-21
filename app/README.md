# Giao diện demo thuật toán Xử lý ảnh

Ứng dụng web nhỏ (Streamlit) giúp trực quan hóa 50 thuật toán của nhóm: **chọn thuật toán → đưa ảnh vào → chạy → xem ảnh kết quả**.

Giao diện **không sửa logic** trong `src/`. Mỗi thuật toán được gọi nguyên trạng qua một lớp bọc trong `app/algorithms.py`. Lớp bọc chỉ chuẩn bị đầu vào (đổi kiểu, tính histogram, nhị phân hóa, chia khối 8×8…) và đổi đầu ra thành ảnh.

## Cài đặt

Dùng Python 3.10 trở lên. Mở terminal tại **thư mục gốc repo**.

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r app/requirements.txt
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt
```

## Chạy giao diện

```powershell
streamlit run app/main.py
```

Trình duyệt tự mở `http://localhost:8501`. Nếu không, hãy mở địa chỉ đó bằng tay. Dừng bằng `Ctrl + C` trong terminal.

## Cách dùng

1. **Thuật toán**: ở thanh bên, chọn nhóm (A, B, C, D, E, F, H) rồi chọn thuật toán. Bên dưới có nguồn slide và ghi chú nếu có.
2. **Tham số**: chỉnh thanh trượt hoặc ô chọn. Mỗi thuật toán nhớ tham số riêng.
3. **Ảnh đầu vào**: chọn *Ảnh mẫu* (tự sinh, có bản nhiễu muối tiêu và nhiễu Gaussian) hoặc *Tải ảnh lên* (PNG, JPG, BMP, TIFF, WEBP). Ảnh được chuyển sang ảnh xám, riêng H01 giữ ảnh màu RGB.
4. Nhấn **▶ Chạy thuật toán**. Màn hình hiện ảnh đầu vào và ảnh kết quả cạnh nhau, kèm bảng thông tin (ngưỡng T, số bit, PSNR…), các ảnh trung gian và nút **Tải ảnh kết quả (PNG)**.

> Các thuật toán viết bằng vòng lặp Python thuần nên ảnh được thu nhỏ theo thanh trượt *Cạnh dài tối đa* (mặc định 256 px). Ảnh lớn hơn sẽ chạy chậm hơn.

## Mỗi thuật toán cho ra ảnh gì

| Mã | Ảnh kết quả | Lớp bọc làm thêm gì |
|---|---|---|
| A01–A06, B01–B07 | Ảnh sau biến đổi / sau lọc | Gọi thẳng hàm gốc. A03 xuất 0/255 để dễ nhìn |
| A07, A08 | Ảnh sau biến đổi / sau cân bằng | Vẽ thêm histogram trước/sau và bảng ánh xạ |
| C01–C04 | Độ lớn gradient (co giãn theo max), hoặc ảnh biên nếu T > 0 | Hiển thị thêm \|Gx\|, \|Gy\| |
| C05 | \|đáp ứng Laplacian\| co giãn theo max | Hàm gốc trả số có dấu |
| C06 | Ảnh sắc nét, cắt về 0..255 | |
| C07 | Ảnh biên Canny | Hiển thị các bước: làm mịn, gradient, sau NMS |
| D01 | Biểu đồ histogram trước/sau làm trơn | Hàm gốc nhận và trả histogram |
| D02–D05 | Ảnh nhị phân | Ảnh → histogram → tìm T → áp ngưỡng bằng A03 |
| D06 | Vùng tô đỏ trên ảnh, seed đánh dấu xanh | Seed chọn theo % chiều cao/rộng; tiêu chuẩn \|mức xám − seed\| ≤ ngưỡng |
| D07 | Ảnh tô theo trung bình từng vùng, biên vùng màu đỏ | Ảnh thu nhỏ (32–64 px). Vùng khởi tạo là các pixel liền kề cùng khoảng mức xám. P(R): max − min ≤ ngưỡng |
| D08, D09 | Như D07 | Ảnh co về N×N, N là lũy thừa của 2 (yêu cầu ở C5 tr.91) |
| E01–E03 | Ảnh giải mã (giống ảnh gốc vì nén không tổn thất) | Báo số loạt, số bit, tỉ số nén. E01/E02 có thêm bản đồ độ dài loạt/độ dài mã |
| E04 | log(1 + \|hệ số DCT\|) từng khối 8×8 | Ảnh dựng lại bằng IDCT |
| E05, E08 | Ảnh dựng lại sau lượng tử hóa | DCT → lượng tử → (RLE với E08) → giải mã → IDCT, báo PSNR |
| E06 | Ảnh dựng lại khi chỉ giữ N hệ số đầu theo zig-zag | Hiển thị thứ tự quét |
| E07 | Ảnh trung bình khối dựng từ DC đã giải mã DPCM | Bản đồ sai phân DC |
| E09 | Ảnh dựng lại qua toàn bộ quy trình JPEG | Báo số bit, tỉ số nén, PSNR |
| F01–F04 | Ảnh nhị phân sau phép hình thái | Ảnh xám → nhị phân (Otsu hoặc ngưỡng tự chọn, có thể đảo) |
| F05 | Ảnh đã lấp lỗ | Tự tìm lỗ (vùng nền không chạm mép) làm seed, hoặc chọn seed theo % |
| H01 | Lượng mực CMY hiển thị như ảnh RGB | Ba kênh C, M, Y và ảnh RGB dựng lại |
| H02 | Ảnh halftone lớn gấp 2 hoặc 4 lần | Đầu vào tối đa 128 px |
| H03 | Ảnh dithering | Chọn ma trận ngưỡng của code hoặc của slide C4 tr.55 |
| H04, H05 | Ảnh khuếch tán lỗi | So sánh với phân ngưỡng thường |

## Lưu ý về code gốc (giữ nguyên, không sửa)

- **H02**: ma trận thứ tự 4×4 trong code là Bayer, khác ma trận Rylander ở C4 tr.51.
- **H04/H05**: pixel bằng ngưỡng cho ra 255, còn A03/H03 dùng phép so sánh "lớn hơn".

## Tự kiểm tra

```powershell
python app/selftest.py
```

Script chạy cả 50 thuật toán, so khớp từng pixel giữa lớp bọc và hàm gốc ở các bài tiêu biểu, và kiểm lại ví dụ slide C3 tr.52 (lọc k giá trị gần nhất: 16 → 8). Kết quả mong đợi: `KẾT QUẢ: ĐẠT`.

## Cấu trúc

```
app/
├── main.py           # giao diện Streamlit
├── algorithms.py     # lớp bọc + bảng đăng ký 50 thuật toán (format chung)
├── samples.py        # ảnh mẫu tự sinh
├── selftest.py       # kiểm tra nhanh
└── requirements.txt
```

Format chung trong `algorithms.py`:

```python
run(ảnh_uint8, **tham_số) -> Result(image=ảnh_uint8, info={...}, extras=[(chú thích, ảnh), ...])
```

### Thêm một thuật toán mới

1. Viết thuật toán trong `src/cum-x/` như bình thường.
2. Trong `app/algorithms.py`, viết hàm `run_xxx(img, ...)` gọi thuật toán đó và trả `Result`.
3. Thêm một dòng `Algorithm("Mã", "Tên", nhóm, run_xxx, [tham số], "nguồn slide")` vào `ALGORITHMS`. Giao diện tự hiện thuật toán mới.
