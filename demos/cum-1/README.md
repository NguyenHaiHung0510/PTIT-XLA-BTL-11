# Demo cụm 1 – Xử lý ảnh

Thư mục `demos/cum-1/` chứa chương trình minh họa cho 15 bài xử lý ảnh thuộc cụm 1, gồm A01–A08 và B01–B07.

Các chương trình sử dụng thuật toán được cài đặt trong `src/cum-1/`. Mỗi demo giúp kiểm tra kết quả xử lý thông qua ma trận giá trị, hình ảnh trước và sau biến đổi hoặc biểu đồ minh họa.

Phần giao diện ứng dụng tổng hợp sẽ được nhóm xây dựng và tích hợp riêng.

## 1. Hướng dẫn cài đặt và chạy chương trình

### Yêu cầu

- Python 3.
- Các thư viện: NumPy, Pillow, Matplotlib và pytest.

### Cài đặt thư viện

Mở Terminal tại thư mục gốc của dự án và chạy:

```powershell
pip install -r src/cum-1/requirements.txt
```

### Chạy chương trình minh họa

Ví dụ, để chạy bài A01:

```powershell
python demos/cum-1/demo_A01.py
```

Các bài còn lại thực hiện tương tự bằng cách thay mã bài tương ứng.

Một số demo hỗ trợ sử dụng ảnh `sample.jpg` đặt trong thư mục `demos/cum-1/`. Nếu không có ảnh này, chương trình sẽ dùng dữ liệu hoặc ảnh minh họa được tạo sẵn.

### Chạy kiểm thử

Để kiểm tra toàn bộ 15 thuật toán, sử dụng lệnh:

```powershell
python -m pytest tests/cum-1/ -q
```

Bộ kiểm thử hiện tại gồm 125 trường hợp, dùng để kiểm tra kết quả tính toán, dữ liệu đầu vào và một số trường hợp đặc biệt của các thuật toán.

---

## 2. Các bài biến đổi mức xám và Histogram

### A01 – Biến đổi âm bản

**Nguồn:** `sources/slides/c3.pdf`, trang PDF 13.

**Mô tả:** Biến đổi âm bản đảo ngược mức sáng của ảnh. Những vùng sáng sẽ trở thành tối và ngược lại.

- **Đầu vào:** Ma trận ảnh xám với mức xám từ 0 đến 255.
- **Đầu ra:** Ma trận ảnh âm bản.
- **Công thức:** `s = 255 - r`.

Trong đó, `r` là mức xám ban đầu và `s` là mức xám sau biến đổi.

**Cách chạy:**

```powershell
python demos/cum-1/demo_A01.py
```

**Kết quả minh họa:**

- In ma trận ảnh trước và sau biến đổi.
- Hiển thị ảnh gốc và ảnh âm bản để so sánh.
- Có thể sử dụng ảnh `sample.jpg` hoặc ảnh gradient mặc định.

### A02 – Biến đổi tuyến tính độ sáng

**Nguồn:** `sources/slides/c3.pdf`, trang PDF 18.

**Mô tả:** Điều chỉnh độ sáng của ảnh bằng cách nhân mức xám của từng pixel với một hệ số.

- **Đầu vào:** Ma trận ảnh xám và hệ số `c ≥ 0`.
- **Đầu ra:** Ma trận ảnh sau khi điều chỉnh độ sáng.
- **Công thức:** `s = c × r`.

Ý nghĩa của hệ số `c`:

- `c > 1`: Tăng độ sáng.
- `0 ≤ c < 1`: Giảm độ sáng.
- `c = 1`: Giữ nguyên ảnh.

Giá trị sau biến đổi được giới hạn trong khoảng 0–255 và làm tròn đến số nguyên gần nhất, với trường hợp `.5` làm tròn lên.

**Cách chạy:**

```powershell
python demos/cum-1/demo_A02.py
```

**Kết quả minh họa:**

- In ma trận ảnh gốc và ma trận sau biến đổi.
- Hiển thị ba ảnh: ảnh gốc, ảnh tăng sáng và ảnh giảm sáng.
- So sánh ảnh hưởng của hệ số `c` đến độ sáng.

### A03 – Phân ngưỡng cố định

**Nguồn:** `sources/slides/c3.pdf`, trang PDF 14.

**Mô tả:** Chuyển ảnh xám thành ảnh nhị phân dựa trên một giá trị ngưỡng `T` cho trước.

- **Đầu vào:** Ma trận ảnh xám và ngưỡng `T`.
- **Đầu ra:** Ma trận ảnh nhị phân.

Quy tắc phân ngưỡng:

- Nếu `r > T` thì pixel đầu ra bằng `1`.
- Nếu `r ≤ T` thì pixel đầu ra bằng `0`.

Chương trình cũng hỗ trợ biểu diễn kết quả bằng hai mức 0 và 255 để hiển thị ảnh đen trắng.

**Cách chạy:**

```powershell
python demos/cum-1/demo_A03.py
```

**Kết quả minh họa:**

- In ma trận ảnh trước và sau phân ngưỡng.
- Hiển thị ảnh gốc và ảnh nhị phân.
- Có thể dùng ảnh `sample.jpg` hoặc ảnh gradient mặc định.

### A04 – Biến đổi Log và Log ngược

**Nguồn:** `sources/slides/c3.pdf`, trang PDF 15–17.

**Mô tả:** Biến đổi Log làm nổi bật các mức xám thấp, trong khi phép biến đổi ngược có tác dụng ngược lại trên thang mức xám đã chuẩn hóa.

- **Đầu vào:** Ma trận ảnh xám 0–255.
- **Đầu ra:** Ma trận ảnh sau biến đổi Log hoặc Log ngược.

Công thức Log:

`s = c × ln(1 + r)`

Công thức ngược tương ứng:

`r = exp(s / c) - 1`

Hệ số chuẩn hóa:

`c = 255 / ln(256)`

Kết quả được giới hạn trong khoảng 0–255 và làm tròn `.5` lên.

**Cách chạy:**

```powershell
python demos/cum-1/demo_A04.py
```

**Kết quả minh họa:**

- In ma trận ảnh gốc và kết quả của hai phép biến đổi.
- Hiển thị ba ảnh: ảnh gốc, ảnh sau biến đổi Log và ảnh sau biến đổi Log ngược.
- Quan sát sự thay đổi độ sáng ở các vùng có mức xám khác nhau.

### A05 – Biến đổi lũy thừa Gamma

**Nguồn:** `sources/slides/c3.pdf`, trang PDF 18–20.

**Mô tả:** Điều chỉnh độ sáng và phân bố mức xám của ảnh bằng phép biến đổi Gamma.

- **Đầu vào:** Ma trận ảnh xám 0–255 và hệ số `gamma > 0`.
- **Đầu ra:** Ma trận ảnh sau biến đổi Gamma.

Công thức tổng quát:

`s = c × r^gamma`

Công thức chuẩn hóa cho ảnh 8-bit:

`s = 255 × (r / 255)^gamma`

Với công thức chuẩn hóa trên:

- `gamma < 1`: Ảnh sáng hơn.
- `gamma > 1`: Ảnh tối hơn.
- `gamma = 1`: Ảnh không thay đổi.

Kết quả được làm tròn `.5` lên và giới hạn trong khoảng 0–255.

**Cách chạy:**

```powershell
python demos/cum-1/demo_A05.py
```

**Kết quả minh họa:**

- In ma trận ảnh và kết quả với `gamma = 0.5` và `gamma = 2.0`.
- Hiển thị ba ảnh để so sánh độ sáng.
- Có thể dùng ảnh `sample.jpg` hoặc ảnh gradient mặc định.

### A06 – Kéo giãn tương phản theo từng đoạn

**Nguồn:** `sources/slides/c3.pdf`, trang PDF 21.

**Mô tả:** Điều chỉnh độ tương phản của ảnh bằng hàm biến đổi tuyến tính gồm ba đoạn.

- **Đầu vào:** Ma trận ảnh xám và hai điểm điều khiển `(r1, s1)`, `(r2, s2)`.
- **Đầu ra:** Ma trận ảnh sau kéo giãn tương phản.
- **Phương pháp:** Nội suy tuyến tính theo ba đoạn của hàm biến đổi mức xám.

Các tham số mặc định:

- `r1 = 80`, `s1 = 30`.
- `r2 = 160`, `s2 = 220`.

Kết quả được giới hạn trong khoảng 0–255 và làm tròn `.5` lên.

**Cách chạy:**

```powershell
python demos/cum-1/demo_A06.py
```

**Kết quả minh họa:**

- In ma trận ảnh trước và sau xử lý.
- Hiển thị ảnh gốc và ảnh sau khi điều chỉnh tương phản.
- Vẽ đồ thị hàm biến đổi mức xám.
- Có thể dùng ảnh `sample.jpg` hoặc ảnh gradient mặc định.

### A07 – Histogram và biến đổi Histogram

**Nguồn:** `sources/slides/c3.pdf`, trang PDF 23–31.

**Liên hệ bài tập:** Câu tự luận 3.1 và 3.2.

**Mô tả:** Xây dựng Histogram để thống kê số lượng pixel ở từng mức xám. Sau đó tính Histogram mới khi ảnh được biến đổi bằng một hàm ánh xạ mức xám.

- **Đầu vào:** Ma trận ảnh xám, số mức xám `L` và hàm ánh xạ (nếu có).
- **Đầu ra:** Histogram, tần suất tương đối của từng mức xám và Histogram sau biến đổi.

Các công thức:

- `h(g)`: Số pixel có mức xám `g`.
- `p(g) = h(g) / (M × N)`.

Trong đó, `M × N` là tổng số pixel của ảnh.

**Cách chạy:**

```powershell
python demos/cum-1/demo_A07.py
```

**Kết quả minh họa:**

- Tính và hiển thị Histogram của ảnh ban đầu.
- Tính Histogram sau phép biến đổi `f(g) = |g - 4|`.
- Tính Histogram sau phép biến đổi `f(g) = |2g - 9|`.
- In dữ liệu và vẽ biểu đồ để so sánh kết quả.

### A08 – Cân bằng Histogram

**Nguồn:** `sources/slides/c3.pdf`, trang PDF 32–38.

**Liên hệ bài tập:** Câu tự luận 3.4 và 3.5.

**Mô tả:** Cân bằng Histogram là phương pháp phân bố lại các mức xám dựa trên hàm phân phối tích lũy (CDF), nhằm cải thiện độ tương phản của ảnh trong nhiều trường hợp.

- **Đầu vào:** Ma trận ảnh xám và số mức xám `L`.
- **Đầu ra:** Ảnh sau cân bằng, Histogram, CDF và bảng ánh xạ mức xám.

Công thức:

`s(k) = (L - 1) × CDF(k)`

Giá trị ánh xạ được làm tròn `.5` lên và giới hạn trong khoảng từ `0` đến `L - 1`.

**Cách chạy:**

```powershell
python demos/cum-1/demo_A08.py
```

**Kết quả minh họa:**

- In ma trận ảnh trước và sau cân bằng.
- Hiển thị Histogram trước và sau xử lý.
- Tính xác suất tích lũy CDF.
- Hiển thị bảng ánh xạ mức xám.
- Sử dụng dữ liệu từ câu tự luận 3.4 để minh họa phép tính.

---

## 3. Các bài lọc ảnh

### B01 – Lọc trung bình số học

**Nguồn:** `sources/slides/c3.pdf`, trang PDF 46–48 và 67.

**Mô tả:** Thay giá trị pixel bằng trung bình cộng của các pixel trong cửa sổ lân cận. Phương pháp này có tác dụng làm mịn ảnh và giảm một số loại nhiễu.

- **Đầu vào:** Ma trận ảnh xám 0–255 và kích thước cửa sổ lọc.
- **Đầu ra:** Ma trận ảnh sau lọc trung bình.
- **Công thức:** Lấy tổng các giá trị trong cửa sổ rồi chia cho số pixel của cửa sổ.

Quy ước:

- Kích thước cửa sổ là số lẻ, từ 3 trở lên.
- Các vị trí nằm ngoài biên ảnh được bổ sung giá trị 0 (zero padding).
- Kết quả được làm tròn `.5` lên.

**Cách chạy:**

```powershell
python demos/cum-1/demo_B01.py
```

**Kết quả minh họa:**

- Tính giá trị pixel tâm theo ví dụ ở trang PDF 47.
- Giá trị trung bình tại pixel minh họa là `98.3333`, sau làm tròn được `98`.
- Hiển thị ảnh gốc, ảnh sau lọc 3×3 và 5×5.
- Có thể dùng ảnh `sample.jpg` hoặc ảnh minh họa mặc định.

### B02 – Lọc trung bình có trọng số và lọc Gaussian

**Nguồn:**

- `sources/slides/c3.pdf`, trang PDF 49.
- `sources/slides/c5.pdf`, trang PDF 40.

**Mô tả:** Tính giá trị pixel mới bằng trung bình có trọng số của các pixel trong cửa sổ. Các pixel có thể được gán trọng số khác nhau tùy theo vị trí.

- **Đầu vào:** Ma trận ảnh xám 0–255 và bộ trọng số.
- **Đầu ra:** Ảnh sau lọc trung bình có trọng số hoặc lọc Gaussian.

Các bộ lọc được minh họa:

- Bộ lọc trọng số 3×3, tổng trọng số bằng 16.
- Bộ lọc Gaussian xấp xỉ 5×5, tổng trọng số bằng 159.

Quy ước:

- Padding bằng 0.
- Kết quả được làm tròn `.5` lên và giới hạn trong khoảng 0–255.
- Phần tính toán bộ lọc được cài đặt bằng Python và NumPy.

**Cách chạy:**

```powershell
python demos/cum-1/demo_B02.py
```

**Kết quả minh họa:**

- In ma trận ảnh và các bộ trọng số sử dụng.
- Hiển thị kết quả lọc trọng số 3×3 và Gaussian 5×5.
- So sánh ảnh gốc với các ảnh sau xử lý.
- Có thể sử dụng ảnh `sample.jpg` hoặc ảnh nhiễu mặc định.

### B03 – Lọc trung bình k giá trị gần nhất có ngưỡng

**Nguồn:** `sources/slides/c3.pdf`, trang PDF 50–52.

**Mô tả:** Chọn `k` giá trị mức xám gần với pixel tâm nhất trong cửa sổ, tính trung bình và sử dụng ngưỡng để quyết định có thay đổi pixel tâm hay không.

- **Đầu vào:** Ma trận ảnh xám, số lượng `k`, ngưỡng `theta` và kích thước cửa sổ.
- **Đầu ra:** Ma trận ảnh sau lọc.

Nguyên tắc thực hiện:

1. Xét các pixel trong cửa sổ, bao gồm pixel tâm.
2. Chọn `k` giá trị có khoảng cách mức xám nhỏ nhất so với pixel tâm.
3. Tính trung bình của `k` giá trị đã chọn.
4. Nếu độ chênh lệch giữa pixel tâm và giá trị trung bình lớn hơn `theta`, thay pixel tâm bằng giá trị trung bình; ngược lại giữ nguyên.

Quy ước:

- Padding bằng 0.
- Khi các giá trị có cùng khoảng cách, ưu tiên mức xám lớn hơn.
- Kết quả được làm tròn `.5` lên và giới hạn trong khoảng 0–255.

**Cách chạy:**

```powershell
python demos/cum-1/demo_B03.py
```

**Kết quả minh họa:**

- Sử dụng ví dụ trong slide, pixel tâm có giá trị `16` được thay bằng `8`.
- In ma trận ảnh trước và sau lọc.
- Hiển thị ảnh nhiễu và ảnh đã xử lý.
- Hỗ trợ ảnh `sample.jpg` hoặc dữ liệu minh họa mặc định.

### B04 – Lọc trung vị (Median Filter)

**Nguồn:** `sources/slides/c3.pdf`, trang PDF 53–54 và 70.

**Mô tả:** Thay pixel tâm bằng giá trị trung vị của các pixel trong cửa sổ. Bộ lọc này đặc biệt phù hợp để giảm nhiễu muối tiêu.

- **Đầu vào:** Ma trận ảnh xám 0–255 và kích thước cửa sổ.
- **Đầu ra:** Ma trận ảnh sau lọc trung vị.

Các bước thực hiện:

1. Lấy các pixel trong cửa sổ lân cận.
2. Sắp xếp các giá trị theo thứ tự tăng dần.
3. Chọn giá trị ở giữa để thay thế pixel tâm.

Quy ước:

- Sử dụng cửa sổ kích thước lẻ.
- Padding bằng 0.

**Cách chạy:**

```powershell
python demos/cum-1/demo_B04.py
```

**Kết quả minh họa:**

- Minh họa ma trận có pixel tâm `255`, sau lọc được `12`.
- Hiển thị ảnh có nhiễu muối tiêu.
- So sánh kết quả lọc trung vị 3×3 và 5×5.
- Có thể sử dụng ảnh `sample.jpg` hoặc ảnh nhiễu mặc định.

### B05 – Lọc Min (Minimum Filter)

**Nguồn:** `sources/slides/c3.pdf`, trang PDF 42 và 71.

**Mô tả:** Thay pixel tâm bằng giá trị nhỏ nhất trong cửa sổ lân cận. Bộ lọc Min thường được sử dụng để giảm nhiễu muối, tức các điểm trắng bất thường.

- **Đầu vào:** Ma trận ảnh xám 0–255 và kích thước cửa sổ.
- **Đầu ra:** Ma trận ảnh sau lọc Min.
- **Công thức:** `Giá trị mới = Min(các pixel trong cửa sổ)`.

Quy ước:

- Kích thước cửa sổ là số lẻ.
- Padding bằng 0.

**Cách chạy:**

```powershell
python demos/cum-1/demo_B05.py
```

**Kết quả minh họa:**

- Minh họa pixel tâm `255` được thay bằng `98`.
- Hiển thị ảnh có các điểm nhiễu trắng.
- So sánh ảnh sau lọc Min 3×3 và 5×5.
- Có thể sử dụng ảnh `sample.jpg` hoặc ảnh mặc định.

### B06 – Lọc Max (Maximum Filter)

**Nguồn:** `sources/slides/c3.pdf`, trang PDF 42 và 71.

**Mô tả:** Thay pixel tâm bằng giá trị lớn nhất trong cửa sổ lân cận. Bộ lọc Max thường được sử dụng để giảm nhiễu tiêu, tức các điểm đen bất thường.

- **Đầu vào:** Ma trận ảnh xám 0–255 và kích thước cửa sổ.
- **Đầu ra:** Ma trận ảnh sau lọc Max.
- **Công thức:** `Giá trị mới = Max(các pixel trong cửa sổ)`.

Quy ước:

- Kích thước cửa sổ là số lẻ.
- Padding bằng 0.

**Cách chạy:**

```powershell
python demos/cum-1/demo_B06.py
```

**Kết quả minh họa:**

- Minh họa pixel tâm `0` được thay bằng `103`.
- Hiển thị ảnh có các điểm nhiễu đen.
- So sánh ảnh sau lọc Max 3×3 và 5×5.
- Có thể sử dụng ảnh `sample.jpg` hoặc ảnh mặc định.

### B07 – Lọc điểm giữa (Midpoint Filter)

**Nguồn:** `sources/slides/c3.pdf`, trang PDF 69 và 72.

**Mô tả:** Thay pixel tâm bằng trung bình cộng của giá trị lớn nhất và nhỏ nhất trong cửa sổ. Bộ lọc điểm giữa có thể hữu ích khi xử lý một số dạng nhiễu có phân bố Gaussian hoặc phân bố đều.

- **Đầu vào:** Ma trận ảnh xám 0–255 và kích thước cửa sổ.
- **Đầu ra:** Ma trận ảnh sau lọc điểm giữa.

Công thức:

`Midpoint = (Min + Max) / 2`

Trong đó `Min` và `Max` lần lượt là mức xám nhỏ nhất và lớn nhất trong cửa sổ.

Quy ước:

- Kích thước cửa sổ là số lẻ.
- Padding bằng 0.
- Kết quả được làm tròn `.5` lên và giới hạn trong khoảng 0–255.

**Cách chạy:**

```powershell
python demos/cum-1/demo_B07.py
```

**Kết quả minh họa:**

- In ma trận ảnh trước và sau lọc.
- Minh họa pixel tâm `150` được thay bằng `120`.
- Hiển thị ảnh có nhiễu Gaussian và kết quả lọc 3×3, 5×5.
- Có thể sử dụng ảnh `sample.jpg` hoặc ảnh minh họa mặc định.

---

## 4. Tổng kết

Cụm 1 đã triển khai 15 thuật toán xử lý ảnh, gồm:

- **A01–A08:** Các phép biến đổi mức xám, Histogram và cân bằng Histogram.
- **B01–B07:** Các bộ lọc trung bình, lọc trung vị, lọc Min, Max và Midpoint.

Mỗi thuật toán có file cài đặt riêng trong `src/cum-1/`, chương trình minh họa trong `demos/cum-1/` và file kiểm thử tương ứng trong `tests/cum-1/`.

Các chương trình demo dùng để kiểm tra trực quan kết quả xử lý. Phần giao diện tổng hợp cho toàn bộ bài tập lớn sẽ do nhóm tích hợp và hoàn thiện.