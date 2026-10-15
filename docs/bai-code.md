# Danh sách bài code

Có **45 đầu việc chính** theo cách chia dưới đây và **5 bài chương 4 optional**, tổng **50 đầu việc để phân công**. Đây là số đầu việc, không phải số thuật toán độc lập hay checklist cô đã xác nhận. A02 theo ghi chú lớp; E09 là ghép demo từ các phần đã có.

Một bài có thể gồm hai chiều mã hóa/giải mã hoặc các biến thể kernel. Đổi tham số, cửa sổ hay ảnh mẫu không tạo bài mới. **Nhẹ/Vừa/Nặng** giúp nhìn độ phức tạp, không dùng để chia đều số bài.

Cột thi đối chiếu [ngân hàng tự luận](../sources/ngan-hang-tu-luan.pdf). **Tính** = có yêu cầu thực hiện phép tính; **Lý thuyết** = hỏi nguyên lý/các bước; **Liên hệ/ví dụ** = hỗ trợ trả lời; **Suy luận** = đề chưa gọi tên phương pháp. Ref dùng trang PDF.

## Biến đổi điểm và histogram

| Mã | Bài | Độ khó | Slide | Thi tự luận |
|---|---|---|---|---|
| A01 | Âm bản | Nhẹ | [C3 tr.13](../sources/slides/c3.pdf#page=13) | Chưa thấy trực tiếp |
| A02 | Biến đổi tuyến tính độ sáng | Nhẹ | [C3 tr.18](../sources/slides/c3.pdf#page=18), gamma=1; ghi chú lớp | Lý thuyết: [1.8](../sources/ngan-hang-tu-luan.pdf#page=1) |
| A03 | Phân ngưỡng cố định | Nhẹ | [C3 tr.14](../sources/slides/c3.pdf#page=14); [C5 tr.64](../sources/slides/c5.pdf#page=64) | Áp ngưỡng sau tìm T: [4.5](../sources/ngan-hang-tu-luan.pdf#page=8), [4.6](../sources/ngan-hang-tu-luan.pdf#page=8) |
| A04 | Biến đổi log và inverse log | Nhẹ | [C3 tr.15-17](../sources/slides/c3.pdf#page=15) | Chưa thấy trực tiếp |
| A05 | Biến đổi lũy thừa gamma | Nhẹ | [C3 tr.18-20](../sources/slides/c3.pdf#page=18) | Chưa thấy trực tiếp |
| A06 | Kéo giãn tương phản theo đoạn | Vừa | [C3 tr.21](../sources/slides/c3.pdf#page=21) | Chưa thấy trực tiếp |
| A07 | Histogram và histogram sau biến đổi mức xám | Vừa | [C3 tr.23-31](../sources/slides/c3.pdf#page=23) | Tính: [3.1](../sources/ngan-hang-tu-luan.pdf#page=3), [3.2](../sources/ngan-hang-tu-luan.pdf#page=3), [3.3](../sources/ngan-hang-tu-luan.pdf#page=3) |
| A08 | Cân bằng histogram | Vừa | [C3 tr.32-38](../sources/slides/c3.pdf#page=32) | Tính: [3.4](../sources/ngan-hang-tu-luan.pdf#page=3), [3.5](../sources/ngan-hang-tu-luan.pdf#page=4) |

## Lọc và khôi phục ảnh

| Mã | Bài | Độ khó | Slide | Thi tự luận |
|---|---|---|---|---|
| B01 | Lọc trung bình số học | Nhẹ | [C3 tr.46-48,67](../sources/slides/c3.pdf#page=46) | Lý thuyết: [2.4](../sources/ngan-hang-tu-luan.pdf#page=2) |
| B02 | Lọc trung bình có trọng số và Gaussian làm mịn | Vừa | [C3 tr.49](../sources/slides/c3.pdf#page=49); [C5 tr.40](../sources/slides/c5.pdf#page=40) | Chưa thấy trực tiếp |
| B03 | Lọc trung bình k giá trị gần nhất | Vừa | [C3 tr.50-52](../sources/slides/c3.pdf#page=50) | Lý thuyết: [2.4](../sources/ngan-hang-tu-luan.pdf#page=2) |
| B04 | Lọc trung vị | Nhẹ | [C3 tr.53-54,70](../sources/slides/c3.pdf#page=53) | Lý thuyết: [2.4](../sources/ngan-hang-tu-luan.pdf#page=2) |
| B05 | Lọc min | Nhẹ | [C3 tr.42,71](../sources/slides/c3.pdf#page=42) | Chưa thấy trực tiếp |
| B06 | Lọc max | Nhẹ | [C3 tr.42,71](../sources/slides/c3.pdf#page=42) | Chưa thấy trực tiếp |
| B07 | Lọc midpoint | Nhẹ | [C3 tr.69,72](../sources/slides/c3.pdf#page=69) | Chưa thấy trực tiếp |

## Biên và làm sắc nét

| Mã | Bài | Độ khó | Slide | Thi tự luận |
|---|---|---|---|---|
| C01 | Gradient bằng sai phân mặt nạ 1D | Nhẹ | [C5 tr.14-16](../sources/slides/c5.pdf#page=14) | Lý thuyết: [2.5](../sources/ngan-hang-tu-luan.pdf#page=2) |
| C02 | Phát hiện biên Roberts | Vừa | [C5 tr.17](../sources/slides/c5.pdf#page=17) | Liên hệ/ví dụ: [2.6](../sources/ngan-hang-tu-luan.pdf#page=2) |
| C03 | Phát hiện biên Prewitt | Vừa | [C5 tr.18-22](../sources/slides/c5.pdf#page=18) | Tính: [4.1](../sources/ngan-hang-tu-luan.pdf#page=6), [4.3](../sources/ngan-hang-tu-luan.pdf#page=7) |
| C04 | Phát hiện biên Sobel | Vừa | [C5 tr.18-19,23-26](../sources/slides/c5.pdf#page=18) | Tính: [4.2](../sources/ngan-hang-tu-luan.pdf#page=6), [4.4](../sources/ngan-hang-tu-luan.pdf#page=7) |
| C05 | Laplacian phát hiện biến thiên và biên | Vừa | [C5 tr.28-30,35](../sources/slides/c5.pdf#page=28) | Tính: [4.1](../sources/ngan-hang-tu-luan.pdf#page=6), [4.2](../sources/ngan-hang-tu-luan.pdf#page=6) |
| C06 | Làm sắc nét bằng Laplacian | Nhẹ | [C5 tr.31-35](../sources/slides/c5.pdf#page=31) | Chưa thấy trực tiếp |
| C07 | Canny | Nặng | [C5 tr.36-49](../sources/slides/c5.pdf#page=36) | Lý thuyết: [2.7](../sources/ngan-hang-tu-luan.pdf#page=2) |

Câu 4.1/4.3 dùng Prewitt; 4.2/4.4 dùng Sobel. Các câu này yêu cầu cộng hai ma trận thành phần theo đề trước khi giải thích ảnh biên; không tự thay bằng công thức độ lớn gradient. Roberts là ví dụ để trả lời 2.6, đề không nêu tên.

## Histogram và phân vùng

| Mã | Bài | Độ khó | Slide | Thi tự luận |
|---|---|---|---|---|
| D01 | Làm trơn histogram | Nhẹ | [C5 tr.62](../sources/slides/c5.pdf#page=62) | Tính: [3.3](../sources/ngan-hang-tu-luan.pdf#page=3) |
| D02 | Tìm ngưỡng Otsu | Vừa | [C5 tr.65-70](../sources/slides/c5.pdf#page=65) | Suy luận Otsu: [4.5](../sources/ngan-hang-tu-luan.pdf#page=8), [4.6](../sources/ngan-hang-tu-luan.pdf#page=8) |
| D03 | Tìm ngưỡng đẳng liệu Isodata | Vừa | [C5 tr.71-75](../sources/slides/c5.pdf#page=71) | Tính: [4.7](../sources/ngan-hang-tu-luan.pdf#page=8), [4.8](../sources/ngan-hang-tu-luan.pdf#page=9) |
| D04 | Tìm ngưỡng đối xứng nền | Vừa | [C5 tr.76-77,79](../sources/slides/c5.pdf#page=76) | Tính: [4.7](../sources/ngan-hang-tu-luan.pdf#page=8), [4.8](../sources/ngan-hang-tu-luan.pdf#page=9) |
| D05 | Tìm ngưỡng tam giác | Vừa | [C5 tr.78](../sources/slides/c5.pdf#page=78) | Lý thuyết: [2.9](../sources/ngan-hang-tu-luan.pdf#page=2) |
| D06 | Phát triển vùng Region growing | Vừa | [C5 tr.85-86](../sources/slides/c5.pdf#page=85) | Chưa thấy trực tiếp |
| D07 | Hợp vùng Region merging | Nặng | [C5 tr.87-88](../sources/slides/c5.pdf#page=87) | Lý thuyết: [2.10](../sources/ngan-hang-tu-luan.pdf#page=2) |
| D08 | Tách vùng bằng quadtree | Vừa | [C5 tr.89-93](../sources/slides/c5.pdf#page=89) | Lý thuyết: [2.10](../sources/ngan-hang-tu-luan.pdf#page=2) |
| D09 | Tách và hợp vùng | Nặng | [C5 tr.94-100](../sources/slides/c5.pdf#page=94) | Lý thuyết: [2.10](../sources/ngan-hang-tu-luan.pdf#page=2) |

Câu 4.5/4.6 chỉ nói tìm ngưỡng tự động; liên hệ với Otsu là suy luận từ slide. A03 là bước áp ngưỡng, không phải cách tự tìm T.

## Nén ảnh

| Mã | Bài | Độ khó | Slide | Thi tự luận |
|---|---|---|---|---|
| E01 | RLC mã hóa và giải mã loạt dài | Vừa | [C6 tr.11-13](../sources/slides/c6.pdf#page=11) | Lý thuyết: [2.15](../sources/ngan-hang-tu-luan.pdf#page=2) |
| E02 | Huffman mã hóa và giải mã | Vừa | [C6 tr.14-22](../sources/slides/c6.pdf#page=14) | Tính: [3.8](../sources/ngan-hang-tu-luan.pdf#page=4), [3.9](../sources/ngan-hang-tu-luan.pdf#page=5) |
| E03 | LZW mã hóa và giải mã | Nặng | [C6 tr.23-30](../sources/slides/c6.pdf#page=23) | Tính: [4.9](../sources/ngan-hang-tu-luan.pdf#page=10) |
| E04 | DCT và IDCT | Vừa | [C6 tr.44-49](../sources/slides/c6.pdf#page=44) | Lý thuyết: [2.16](../sources/ngan-hang-tu-luan.pdf#page=2) |
| E05 | Lượng tử hóa hệ số DCT | Nhẹ | [C6 tr.50-52](../sources/slides/c6.pdf#page=50) | Lý thuyết: [2.16](../sources/ngan-hang-tu-luan.pdf#page=2) |
| E06 | Quét zig-zag và dựng lại block | Nhẹ | [C6 tr.53,55](../sources/slides/c6.pdf#page=53) | Chưa thấy trực tiếp |
| E07 | DPCM cho hệ số DC | Nhẹ | [C6 tr.54,56](../sources/slides/c6.pdf#page=54) | Chưa thấy trực tiếp |
| E08 | RLE cho hệ số AC của JPEG | Vừa | [C6 tr.54,57](../sources/slides/c6.pdf#page=54) | Chưa thấy trực tiếp |
| E09 | Demo quy trình JPEG đơn giản | Nặng | [C6 tr.39-57](../sources/slides/c6.pdf#page=39) | Lý thuyết: [2.16](../sources/ngan-hang-tu-luan.pdf#page=2) |

E09 là demo ghép quy trình JPEG trên ảnh xám, từ các phần E02 và E04–E08; không yêu cầu xây codec file .jpg đầy đủ.

## Hình thái

| Mã | Bài | Độ khó | Slide | Thi tự luận |
|---|---|---|---|---|
| F01 | Co hình Erosion | Vừa | [C7 tr.9-17](../sources/slides/c7.pdf#page=9) | Tính: [3.10](../sources/ngan-hang-tu-luan.pdf#page=5), [3.11](../sources/ngan-hang-tu-luan.pdf#page=5) |
| F02 | Giãn hình Dilation | Vừa | [C7 tr.18-24](../sources/slides/c7.pdf#page=18) | Tính: [3.10](../sources/ngan-hang-tu-luan.pdf#page=5), [3.11](../sources/ngan-hang-tu-luan.pdf#page=5) |
| F03 | Mở hình Opening | Nhẹ | [C7 tr.25-32](../sources/slides/c7.pdf#page=25) | Chưa thấy trực tiếp |
| F04 | Đóng hình Closing | Nhẹ | [C7 tr.33-37](../sources/slides/c7.pdf#page=33) | Chưa thấy trực tiếp |
| F05 | Làm đầy vùng Hole filling | Vừa | [C7 tr.40](../sources/slides/c7.pdf#page=40); DIP 4e §9.5, làm đầy vùng | Chưa thấy trực tiếp |

F05 có đề bài ở C7 tr.40; quy trình giãn có điều kiện cần đọc thêm Digital Image Processing 4e, §9.5, phần Hole Filling.

## Màu và in ảnh optional

| Mã | Bài | Độ khó | Slide | Thi tự luận |
|---|---|---|---|---|
| H01 | Chuyển RGB và CMY **optional** | Nhẹ | [C4 tr.33-35](../sources/slides/c4.pdf#page=33) | Lý thuyết: [1.2](../sources/ngan-hang-tu-luan.pdf#page=1), [2.2](../sources/ngan-hang-tu-luan.pdf#page=2) |
| H02 | Halftoning bằng chọn mẫu Patterning **optional** | Vừa | [C4 tr.49-53](../sources/slides/c4.pdf#page=49) | Liên hệ/ví dụ: [1.5](../sources/ngan-hang-tu-luan.pdf#page=1) |
| H03 | Ordered dithering bằng ma trận ngưỡng **optional** | Vừa | [C4 tr.48,54-55](../sources/slides/c4.pdf#page=48) | Liên hệ/ví dụ: [1.5](../sources/ngan-hang-tu-luan.pdf#page=1) |
| H04 | Khuếch tán lỗi 1D **optional** | Vừa | [C4 tr.56-60](../sources/slides/c4.pdf#page=56) | Tính: [3.6](../sources/ngan-hang-tu-luan.pdf#page=4), [3.7](../sources/ngan-hang-tu-luan.pdf#page=4) |
| H05 | Khuếch tán lỗi 2D **optional** | Vừa | [C4 tr.61-62](../sources/slides/c4.pdf#page=61) | Lý thuyết: [1.7](../sources/ngan-hang-tu-luan.pdf#page=1) |

Ưu tiên **H01 RGB↔CMY** và **H04 khuếch tán lỗi 1D**. Optional cho BTL; màu, halftone và khuếch tán lỗi vẫn nằm trong ngân hàng ôn thi.

## Bổ sung

Các mục dưới nhận riêng khi cần; không cộng vào 50 đầu việc trên.

| Mã | Bài | Trạng thái | Nguồn và thi |
|---|---|---|---|
| J01 | Lọc trung bình hình học | Tên/ảnh so sánh; cần làm rõ có thuộc full không | [C3 tr.68,75](../sources/slides/c3.pdf#page=68); DIP 4e tr.PDF 330; Chưa thấy trực tiếp |
| J02 | Lọc alpha-trimmed mean | Tên/ảnh so sánh; cần làm rõ có thuộc full không | [C3 tr.75](../sources/slides/c3.pdf#page=75); DIP 4e tr.PDF 334; Chưa thấy trực tiếp |
| J03 | Laplacian of Gaussian LoG | Tên/ảnh so sánh; cần làm rõ có thuộc full không | [C5 tr.12,50-52](../sources/slides/c5.pdf#page=12); Chưa thấy trực tiếp |
| J04 | Difference of Gaussian DoG | Tên/ảnh so sánh; cần làm rõ có thuộc full không | [C5 tr.12](../sources/slides/c5.pdf#page=12); Chưa thấy trực tiếp |
| P01 | Demo lấy mẫu không gian | Demo khái niệm nền | [C2 tr.23-24,32-33](../sources/slides/c2.pdf#page=23); Chưa thấy trực tiếp |
| P02 | Demo lượng tử hóa mức xám | Demo khái niệm nền | [C2 tr.34-35](../sources/slides/c2.pdf#page=34); Chưa thấy trực tiếp |
| R01 | K-means K trung bình | Học lý thuyết cho thi; code mở rộng | [NH tr.2](../sources/ngan-hang-tu-luan.pdf#page=2); Lý thuyết: [2.11](../sources/ngan-hang-tu-luan.pdf#page=2) |
| R02 | KNN K láng giềng để phân loại | Học lý thuyết cho thi; code mở rộng | [NH tr.2](../sources/ngan-hang-tu-luan.pdf#page=2); Lý thuyết: [2.12](../sources/ngan-hang-tu-luan.pdf#page=2) |
| R03 | Mạng Hopfield | Học lý thuyết cho thi; code mở rộng | [NH tr.2](../sources/ngan-hang-tu-luan.pdf#page=2); Lý thuyết: [2.13](../sources/ngan-hang-tu-luan.pdf#page=2) |
| R04 | Mạng Kohonen SOM | Học lý thuyết cho thi; code mở rộng | [NH tr.2](../sources/ngan-hang-tu-luan.pdf#page=2); Lý thuyết: [2.14](../sources/ngan-hang-tu-luan.pdf#page=2) |
| T01 | Trung vị có trọng số | Biến thể từ trắc nghiệm cũ | [TN tr.2](../sources/de-trac-nghiem-2021.pdf#page=2); TN câu 8 |
| T02 | Trung bình có ngưỡng theta | Biến thể từ trắc nghiệm cũ | [TN tr.2](../sources/de-trac-nghiem-2021.pdf#page=2); TN câu 9 |
| T03 | Trung vị có ngưỡng theta | Biến thể từ trắc nghiệm cũ | [TN tr.9](../sources/de-trac-nghiem-2021.pdf#page=9); TN câu 38 |

KNN phân loại R02 khác bộ lọc k giá trị gần nhất B03. Bốn phương pháp J01–J04 cần làm rõ khi cô yêu cầu “full”. Phần dùng chung gồm đọc/hiển thị ảnh, cửa sổ/padding, nhân chập/tương quan và tạo nhiễu minh họa.
