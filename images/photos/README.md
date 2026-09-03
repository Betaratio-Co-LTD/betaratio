# Thư mục ảnh thật — hướng dẫn sử dụng

Đây là nơi bỏ ảnh thật vào để **thay thế tự động** các icon minh họa (SVG) hiện có trên website. Bạn không cần sửa code — chỉ cần:

1. Đặt file ảnh vào đúng thư mục con, **đặt tên file đúng như liệt kê bên dưới** (không dấu, không cần viết hoa).
2. Chạy lại `python3 build.py` ở thư mục gốc của site (hoặc nhờ Claude chạy giúp).
3. Trang nào có ảnh khớp tên sẽ tự động hiển thị ảnh thật thay cho icon. Trang nào chưa có ảnh sẽ **tự động giữ nguyên icon minh họa đẹp** như hiện tại — không bị vỡ layout.

Định dạng file được nhận diện: `.jpg`, `.jpeg`, `.png`, `.webp` (chỉ cần đúng 1 định dạng, đúng tên).
Khuyến nghị nén ảnh dưới ~500KB/ảnh để trang tải nhanh (dùng TinyPNG hoặc Squoosh trước khi bỏ vào).

## Các thư mục (theo mức độ quan trọng)

| Thư mục | Số ảnh | Ưu tiên | Dùng ở đâu |
|---|---|---|---|
| `hero/` | 1 | ★★★ Nên có | Ảnh nền lớn trang chủ (banner) |
| `industries/` | 5 | ★★★ Nên có | Ảnh đại diện 5 ngành (trang chủ + trang "Ngành công nghiệp") |
| `process/` | 3 | ★★☆ Khuyến khích | Ảnh quy trình sản xuất/gia công (trang chủ + trang "Gia công theo yêu cầu") |
| `case-studies/` | 3 | ★★☆ Khuyến khích | Ảnh minh họa case study (trang "Tài nguyên kỹ thuật") |
| `products/` | tùy chọn (tối đa 36) | ★☆☆ Tùy chọn | Ảnh từng sản phẩm cụ thể trên các thẻ sản phẩm nhỏ |

Chi tiết tên file + mô tả nội dung nằm trong `README.md` (hoặc `.txt`) của từng thư mục con.

## Không có ảnh máy chủ nào bị xóa mất

Cơ chế này chỉ **thêm** — nếu bạn không bỏ ảnh nào vào, hoặc chỉ bỏ một phần (ví dụ chỉ có 3/5 ảnh ngành), site vẫn build và chạy bình thường với icon cho các vị trí còn thiếu.
