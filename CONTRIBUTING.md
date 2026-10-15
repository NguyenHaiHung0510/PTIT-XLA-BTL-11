# Làm việc trên repo

Mỗi người chọn một cụm trong [bảng phân công](docs/chia-viec.md) và tự làm song song.

1. Dùng nhánh riêng, ví dụ `cum-1`; pull bản mới trước khi cập nhật.
2. Đặt code trong `src/cum-1/`, ví dụ trong `demos/cum-1/` (đổi số theo cụm). Ghi mã bài, nguồn slide và cách chạy.
3. Có ví dụ nhỏ và kết quả để người đọc nhìn được thuật toán.
4. Push phần đã làm lên repo. Nếu mở PR, người làm có thể tự merge; không yêu cầu reviewer.

Tự viết logic chính, dùng thư viện hỗ trợ; chạy được và giải thích được. Có thể dùng AI hỗ trợ, người làm chịu trách nhiệm phần của mình.

Dùng số có dấu/số thực khi tính trung gian. Theo ghi chú lớp: padding mặc định 0, k-nearest hòa khoảng cách ưu tiên mức xám lớn hơn; làm tròn theo bài đang giải. Ghi rõ các lựa chọn đó nếu chúng ảnh hưởng kết quả.

Không commit môi trường ảo, cache, đầu ra khổng lồ hoặc tài liệu riêng. Giữ nguyên PDF nguồn; ghi chú và lời giải viết riêng.
