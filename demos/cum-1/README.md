
# Demo cụm 1

Thư mục chứa các ví dụ chạy thử cho 15 bài A01–A08 và B01–B07.

Các demo sử dụng thuật toán từ `src/cum-1/` để hiển thị đầu vào và kết quả xử lý.

Giao diện ứng dụng tổng hợp sẽ được thực hiện chung cho cả nhóm.

## A01 - Biến đổi âm bản

- Nguồn: `sources/slides/c3.pdf`, trang PDF 13
- Input: Ma trận ảnh xám, mức xám 0–255
- Output: Ma trận ảnh âm bản
- Công thức: `s = 255 - r`

### Cách chạy

```powershell
python demos/cum-1/demo_A01.py
```

### Kết quả

- Hiển thị ma trận đầu vào và đầu ra.
- Hiển thị ảnh gốc và ảnh âm bản.
- Có thể dùng ảnh `sample.jpg` hoặc ảnh gradient mặc định.


## A02 - Biến đổi tuyến tính độ sáng

- Nguồn: `sources/slides/c3.pdf`, trang PDF 18.
- Công thức: `s = c * r` (gamma = 1).
- Input: Ma trận ảnh xám và hệ số c >= 0.
- Output: Ma trận ảnh xám sau điều chỉnh độ sáng.
- Quy ước: Chặn 0–255, làm tròn .5 lên.

### Cách chạy

```powershell
python demos/cum-1/demo_A02.py
```

### Kết quả

- Ma trận ảnh gốc.
- Ma trận sau tăng và giảm độ sáng.
- Ba ảnh trực quan: gốc, tăng sáng, giảm sáng.

## A03 - Phân ngưỡng cố định

- Nguồn: `sources/slides/c3.pdf`, trang PDF 14.
- Input: Ảnh xám và ngưỡng T.
- Output: Ảnh nhị phân có giá trị 0/1 theo slide.
- Điều kiện: Pixel > T nhận 1, ngược lại nhận 0.
- Hỗ trợ xuất 0/255 để hiển thị ảnh 8-bit.

### Cách chạy

```powershell
python demos/cum-1/demo_A03.py
```

### Kết quả

- Hiển thị ma trận trước và sau phân ngưỡng.
- Visualize ảnh gốc và ảnh đen trắng.
- Có thể sử dụng sample.jpg hoặc ảnh gradient mặc định.
## A04 - Biến đổi Log và Inverse Log

- Nguồn: `sources/slides/c3.pdf`, trang PDF 15–17.
- Input: Ma trận ảnh xám 0–255.
- Output: Ma trận ảnh sau biến đổi Log hoặc Inverse Log.
- Log: `s = c * ln(1 + r)`.
- Inverse Log: `r = exp(s / c) - 1`.
- Hệ số chuẩn hóa: `c = 255 / ln(256)`.
- Làm tròn 0.5 lên, giới hạn mức xám 0–255.

### Cách chạy

python demos/cum-1/demo_A04.py

### Kết quả

- Ma trận gốc và hai ma trận biến đổi.
- Ba hình trực quan: Original, Log, Inverse Log.

## A05 - Biến đổi lũy thừa Gamma

- Nguồn: `sources/slides/c3.pdf`, trang PDF 18–20.
- Input: Ma trận ảnh xám 0–255 và gamma > 0.
- Output: Ma trận ảnh xám sau biến đổi Gamma.
- Công thức tổng quát: `s = c * r^gamma`.
- Chuẩn hóa 8-bit: `s = 255 * (r / 255)^gamma`.
- Làm tròn 0.5 lên, giới hạn mức xám 0–255.

### Cách chạy

python demos/cum-1/demo_A05.py

### Kết quả

- Ma trận đầu vào và kết quả với gamma 0.5, 2.0.
- Hiển thị ba ảnh: gốc, tăng sáng và giảm sáng.
- Hỗ trợ sample.jpg hoặc ảnh gradient mặc định.

## A06 - Kéo giãn tương phản theo đoạn

- Nguồn: `sources/slides/c3.pdf`, trang PDF 21.
- Input: Ảnh xám 0–255 và các điểm điều khiển (r1,s1), (r2,s2).
- Output: Ảnh xám sau kéo giãn tương phản.
- Phương pháp: Hàm tuyến tính gồm 3 đoạn.
- Tham số mặc định: r1=80, s1=30, r2=160, s2=220.
- Làm tròn 0.5 lên và giới hạn trong 0–255.

### Cách chạy

python demos/cum-1/demo_A06.py

### Kết quả

- In ma trận ảnh trước và sau xử lý.
- Hiển thị ảnh gốc và ảnh đã tăng tương phản.
- Hiển thị đồ thị hàm biến đổi mức xám.
- Hỗ trợ sample.jpg hoặc ảnh gradient mặc định.

## A07 - Histogram và histogram sau biến đổi mức xám

- Nguồn: `sources/slides/c3.pdf`, trang PDF 23–31.
- Liên hệ câu tự luận: 3.1, 3.2.
- Input: Ma trận ảnh xám và số mức xám L.
- Output: Histogram h(g), tần suất p(g) và histogram sau biến đổi.
- Công thức: h(g) đếm số pixel mức xám g; p(g) = h(g)/(M*N).
- Có thể truyền hàm ánh xạ f(g) để tính histogram mới.

### Cách chạy

python demos/cum-1/demo_A07.py

### Kết quả

- Histogram của ảnh gốc.
- Histogram sau f(g) = |g-4|.
- Histogram sau f(g) = |2g-9|.
- Biểu đồ và ma trận trực quan cho từng trường hợp.

## A08 - Cân bằng Histogram

- Nguồn: `sources/slides/c3.pdf`, trang PDF 32–38.
- Liên hệ câu tự luận: 3.4, 3.5.
- Input: Ma trận ảnh xám và số mức xám L.
- Output: Ảnh sau cân bằng, histogram, CDF và bảng ánh xạ.
- Công thức: s(k) = (L-1) * CDF(k).
- Quy ước: Làm tròn 0.5 lên, chặn trong [0, L-1].

### Cách chạy

python demos/cum-1/demo_A08.py

### Kết quả

- Ma trận ảnh trước và sau cân bằng.
- Histogram trước và sau cân bằng.
- Xác suất tích lũy CDF.
- Bảng ánh xạ mức xám.
- Demo sử dụng dữ liệu câu tự luận 3.4.

## B01 - Lọc trung bình số học

- Nguồn: `sources/slides/c3.pdf`, trang PDF 46–48, 67.
- Input: Ma trận ảnh xám 0–255, kích thước cửa sổ lẻ.
- Output: Ảnh sau lọc trung bình số học.
- Công thức: Trung bình tất cả pixel trong cửa sổ.
- Padding: 0.
- Làm tròn: 0.5 lên số nguyên kế tiếp.

### Cách chạy

python demos/cum-1/demo_B01.py

### Kết quả

- Demo ma trận theo ví dụ slide trang 47.
- Giá trị trung bình pixel tâm là 98.3333.
- Visualize ảnh gốc, ảnh lọc 3x3 và ảnh lọc 5x5.
- Hỗ trợ sample.jpg hoặc ảnh minh họa mặc định.

## B02 - Lọc trung bình có trọng số và Gaussian

- Nguồn: `sources/slides/c3.pdf`, trang 49; `sources/slides/c5.pdf`, trang 40.
- Input: Ma trận ảnh xám 0–255.
- Output: Ảnh sau lọc trọng số hoặc Gaussian.
- Kernel trọng số: 3x3, tổng trọng số 16.
- Kernel Gaussian xấp xỉ: 5x5, tổng trọng số 159.
- Padding: 0.
- Làm tròn: 0.5 lên, giới hạn 0–255.
- Logic lọc được tự cài đặt bằng Python và NumPy.

### Cách chạy

python demos/cum-1/demo_B02.py

### Kết quả

- In ma trận gốc, hai kernel và kết quả lọc.
- Visualize ảnh gốc, lọc trọng số 3x3 và Gaussian 5x5.
- Có thể sử dụng sample.jpg hoặc ảnh nhiễu mặc định.

## B03 - Lọc trung bình k giá trị gần nhất có ngưỡng

- Nguồn: `sources/slides/c3.pdf`, trang PDF 50–52.
- Input: Ma trận ảnh xám, k, theta và kích thước cửa sổ.
- Output: Ảnh sau lọc trung bình k giá trị gần nhất.
- Quy tắc: Chọn k mức xám gần pixel tâm nhất, bao gồm pixel tâm.
- Nếu chênh lệch trung bình > theta thì thay pixel tâm.
- Padding: 0.
- Hòa khoảng cách: Ưu tiên mức xám lớn hơn.
- Làm tròn: 0.5 lên, giới hạn 0–255.

### Cách chạy

python demos/cum-1/demo_B03.py

### Kết quả

- Demo đúng ví dụ slide: pixel 16 chuyển thành 8.
- In ma trận ảnh trước và sau lọc.
- Visualize ảnh nhiễu và ảnh đã xử lý.
- Hỗ trợ sample.jpg hoặc ảnh minh họa mặc định.
## B04 - Lọc trung vị (Median Filter)

- Nguồn: `sources/slides/c3.pdf`, trang PDF 53–54, 70.
- Input: Ma trận ảnh xám 0–255 và kích thước cửa sổ lẻ.
- Output: Ảnh sau lọc trung vị.
- Phương pháp: Sắp xếp các pixel trong cửa sổ, chọn giá trị giữa.
- Padding: 0.
- Mục đích: Giảm nhiễu muối tiêu.

### Cách chạy

python demos/cum-1/demo_B04.py

### Kết quả

- Demo ma trận: pixel tâm 255 chuyển thành 12.
- Visualize ảnh nhiễu và kết quả lọc 3x3, 5x5.
- Hỗ trợ sample.jpg hoặc ảnh nhiễu mặc định.

## B05 - Lọc Min (Minimum Filter)

- Nguồn: `sources/slides/c3.pdf`, trang PDF 42 và 71.
- Input: Ma trận ảnh xám 0–255 và kích thước cửa sổ lẻ.
- Output: Ảnh sau lọc Min.
- Công thức: Lấy giá trị nhỏ nhất trong cửa sổ láng giềng.
- Padding: 0.
- Mục đích: Giảm nhiễu muối (các điểm trắng bất thường).

### Cách chạy

python demos/cum-1/demo_B05.py

### Kết quả

- Demo ma trận: pixel tâm 255 chuyển thành 98.
- Visualize ảnh nhiễu muối và kết quả lọc 3x3, 5x5.
- Hỗ trợ sample.jpg hoặc ảnh minh họa mặc định.

## B06 - Lọc Max (Maximum Filter)

- Nguồn: `sources/slides/c3.pdf`, trang PDF 42 và 71.
- Input: Ma trận ảnh xám 0–255 và kích thước cửa sổ lẻ.
- Output: Ảnh sau lọc Max.
- Công thức: Lấy giá trị lớn nhất trong cửa sổ láng giềng.
- Padding: 0.
- Mục đích: Giảm nhiễu tiêu (các điểm đen bất thường).

### Cách chạy

python demos/cum-1/demo_B06.py

### Kết quả

- Demo ma trận: pixel tâm 0 chuyển thành 103.
- Visualize ảnh nhiễu tiêu và kết quả lọc 3x3, 5x5.
- Hỗ trợ sample.jpg hoặc ảnh minh họa mặc định.

## B07 - Lọc điểm giữa (Midpoint Filter)

- Nguồn: `sources/slides/c3.pdf`, trang PDF 69 và 72.
- Input: Ma trận ảnh xám 0–255, kích thước cửa sổ lẻ.
- Output: Ảnh sau lọc Midpoint.
- Công thức: Midpoint = (Min + Max) / 2.
- Padding: 0.
- Làm tròn: 0.5 lên, giới hạn 0–255.
- Ứng dụng: Xử lý một số loại nhiễu Gaussian và nhiễu đồng nhất.

### Cách chạy

python demos/cum-1/demo_B07.py

### Kết quả

- Ma trận đầu vào và đầu ra.
- Pixel tâm 150 chuyển thành 120.
- Visualize ảnh nhiễu Gaussian, kết quả lọc 3x3 và 5x5.
- Hỗ trợ sample.jpg hoặc ảnh minh họa mặc định.
