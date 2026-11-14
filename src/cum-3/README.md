# Cụm 3 — Nén ảnh, màu và in ảnh

Mỗi file có logic thuật toán và cách chạy riêng. Xem input, đọc hàm chính, chạy rồi mở đường dẫn kết quả hiện trong terminal.

## Chạy

Từ gốc repo, dùng Python 3.10 trở lên:

```powershell
python src/cum-3/code/e02_huffman.py --tiny
python src/cum-3/code/e09_jpeg_demo.py --tiny
python src/cum-3/code/h04_error_diffusion_1d.py --tiny
```

Cả 14 bài đều có `--tiny` chạy bằng thư viện chuẩn. Nếu đưa ảnh PNG/JPG vào, cài Pillow trong môi trường riêng (Windows):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install Pillow
.\.venv\Scripts\python.exe src/cum-3/code/e09_jpeg_demo.py src/cum-3/input/e09/real.png
```

Thay `real.png` bằng ảnh của bạn; thư mục `input/` chỉ là gợi ý để lưu local. Kết quả nằm ở `output/<mã>/<tên>-01/` dưới cụm này. Chạy lại tạo `-02`, `-03`, …; mở `result.json` để xem số liệu và file PNG/BIN đi kèm nếu có.

## Input và kết quả

JSON dùng số, mảng và object thông thường. Ma trận ảnh có hàng trước, cột sau; `0` là đen, `255` là trắng. Với H01, mỗi pixel là `[R,G,B]`.

| File trong `code/` | Input khi bỏ `--tiny` | Mở kết quả để xem |
|---|---|---|
| [e01_rlc.py](code/e01_rlc.py) | Ảnh, file byte, hoặc JSON `{"pixels":[[4,4,8]]}` | Các cặp [độ dài, giá trị], tách theo hàng ảnh; dữ liệu giải mã |
| [e02_huffman.py](code/e02_huffman.py) | Ảnh, file byte, hoặc JSON `{"pixels":[[1,0],[0,1]],"block":[2,2]}` | Tần suất, các lần ghép, bảng mã, bit payload và kiểm giải mã |
| [e03_lzw.py](code/e03_lzw.py) | Như E02, có thể ghi thêm `"alphabet":[[0,0],[0,1],[1,0],[1,1]]` cho block 1×2 | Mã phát, từ điển thêm dần và dữ liệu giải mã |
| [e04_dct.py](code/e04_dct.py) | Ma trận vuông JSON, hoặc ảnh lấy block trên trái tối đa 8×8 | Hệ số DCT 2D, DCT 1D hàng đầu, IDCT và sai số |
| [e05_quantize.py](code/e05_quantize.py) | JSON `{"coefficients":[[25,-25],[5,-4]],"steps":[[10,10],[10,10]]}` | Chia/làm tròn và nhân ngược; đúng nửa đơn vị làm tròn ra xa 0 |
| [e06_zigzag.py](code/e06_zigzag.py) | Ma trận hệ số JSON | Thứ tự quét và ma trận khôi phục |
| [e07_dpcm.py](code/e07_dpcm.py) | Dãy DC JSON, ví dụ `[45,54,48]` | Sai phân và cộng dồn |
| [e08_ac_rle.py](code/e08_ac_rle.py) | Dãy AC JSON đã bỏ DC | Cặp (số 0, hệ số), EOB và dãy khôi phục |
| [e09_jpeg_demo.py](code/e09_jpeg_demo.py) | Ảnh hoặc ma trận xám JSON | Ảnh gốc, ảnh dựng lại, trace block đầu, số bit payload, MAE/RMSE |
| [h01_rgb_cmy.py](code/h01_rgb_cmy.py) | Ảnh hoặc ma trận RGB JSON | Ba kênh lượng mực CMY và ảnh RGB dựng lại |
| [h02_patterning.py](code/h02_patterning.py) | Ảnh, ma trận xám JSON hoặc `{"pixels":[[128]],"cell":4}` | Một pixel thành ô 2×2 (mặc định) hoặc 4×4 |
| [h03_ordered_dither.py](code/h03_ordered_dither.py) | Ảnh, ma trận xám JSON hoặc object có `pixels` và `thresholds` | Kết quả so với ngưỡng lặp theo vị trí |
| [h04_error_diffusion_1d.py](code/h04_error_diffusion_1d.py) | Ảnh, ma trận xám JSON hoặc object có `pixels` và `threshold` | So ngưỡng thường với bù lỗi; trace, bỏ lỗi cuối mỗi hàng |
| [h05_floyd_steinberg.py](code/h05_floyd_steinberg.py) | Như H04 | Trace phân phối lỗi và ảnh nhị phân giữ kích thước |

E01–E03 chuyển ảnh đầu vào sang xám 8 bit trước khi mã hóa; `round_trip` kiểm các ký hiệu xám đó, không bảo toàn màu hoặc byte của file ảnh. Muốn bảo toàn byte file, đưa file không phải ảnh (ví dụ `.txt`/`.bin`). Với JSON, E02/E03 có thể chọn block và bảng ký hiệu theo đề. `decoded.png` giữ nguyên mức xám; `binary-preview.png` riêng giúp nhìn rõ input 0/1.

H04/H05 dùng ngưỡng 127 mặc định; bằng ngưỡng cho 255, chỉ gửi lỗi đến pixel chưa xử lý trong ảnh. Báo cáo dài chỉ hiện phần đầu của một số dãy. E09 là demo JPEG giáo dục trên ảnh xám: kiểm hệ số lượng tử qua khâu mã hóa/giải mã, đo sai lệch pixel sau dựng lại. DC được tính trực tiếp từ tổng pixel; AC dùng số thực gần đúng. Trace DCT của E09 giữ nguyên hệ số thực sự đưa vào lượng tử. Số bit payload không gồm cây mã/metadata; chương trình không xuất codec `.jpg`.

Đối chiếu: [danh sách bài](../../docs/bai-code.md), [slide C6](../../sources/slides/c6.pdf), [slide C4](../../sources/slides/c4.pdf).
