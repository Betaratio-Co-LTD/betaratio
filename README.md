# Website Betaratio

Website tĩnh (HTML/CSS/JS thuần, không cần build tool) cho Betaratio — công ty công nghệ lọc và phân tách công nghiệp. Nội dung được dựng theo bản thiết kế kiến trúc thông tin (sitemap) đã cung cấp, lấy cảm hứng từ cấu trúc website B2B của Donaldson Co.

## 1. Cấu trúc thư mục

```
betaratio-website/
├── index.html                     Trang chủ
├── industries.html                Trang tổng hợp "Ngành công nghiệp"
├── industries/
│   ├── food-beverage.html
│   ├── pharmaceuticals.html
│   ├── electronics.html
│   ├── high-tech-cleanrooms.html
│   └── energy-heavy-industries.html
├── products/
│   ├── index.html                 Trang tổng hợp "Sản phẩm" + ma trận phân loại
│   ├── liquid-filtration.html     Lọc chất lỏng (lõi lọc, túi lọc, vải lọc, bình lọc)
│   └── gas-separation.html        Lọc khí & Sàng lọc
├── custom-oem.html                Năng lực gia công theo yêu cầu (OEM/ODM)
├── resources.html                 Tài nguyên kỹ thuật (catalogue, chứng nhận, case study)
├── about.html                     Về Betaratio
├── contact.html                   Liên hệ & Yêu cầu báo giá (RFQ)
├── 404.html                       Trang lỗi 404 tùy chỉnh
├── css/style.css                  Toàn bộ style (1 file duy nhất)
├── js/main.js                     Menu di động, tab, bộ lọc sản phẩm, form RFQ
├── images/favicon.svg             Favicon
├── robots.txt / sitemap.xml       SEO cơ bản
└── build.py                       Script Python đã dùng để sinh ra các trang HTML
                                    (chỉ là công cụ hỗ trợ dựng trang — KHÔNG cần
                                    Python để chạy website, chỉ cần nếu bạn muốn
                                    sửa hàng loạt trang bằng cách sửa dữ liệu rồi
                                    chạy lại `python3 build.py`)
```

Toàn bộ hình ảnh trong site hiện là **đồ họa minh họa/placeholder** (icon SVG, khối gradient) — xem mục 4 để thay bằng ảnh thật.

## 2. Xem thử trên máy trước khi đưa lên mạng

Không cần cài gì thêm, chỉ cần một static server đơn giản:

```bash
cd betaratio-website
python3 -m http.server 8000
# rồi mở http://localhost:8000 trên trình duyệt
```

(Mở trực tiếp file `index.html` bằng trình duyệt cũng xem được gần như đầy đủ, nhưng nên dùng server ở trên để đường dẫn hoạt động chính xác 100%.)

## 3. Đưa lên GitHub

### Cách A — Dùng Git (khuyến nghị nếu máy bạn đã cài Git)

> **Lưu ý:** thư mục này đã có sẵn một Git repo cục bộ với 1 commit ban đầu (đã chạy sẵn `git init` + `git add` + `git commit`, nhánh `main`). Nếu bạn giữ nguyên thư mục này (không giải nén lại kiểu mất thư mục `.git` ẩn), bạn có thể **bỏ qua bước `git init/add/commit`** bên dưới và chỉ cần làm 2 dòng cuối (thêm remote rồi push).

1. Tạo repo mới trên GitHub: vào [github.com/new](https://github.com/new), đặt tên (ví dụ `betaratio-website`), **không** tick "Add a README" (vì mình đã có sẵn), bấm **Create repository**.
2. Trong terminal, tại thư mục `betaratio-website`:

   ```bash
   git init
   git add .
   git commit -m "Initial commit: Betaratio website"
   git branch -M main
   git remote add origin https://github.com/<ten-tai-khoan>/<ten-repo>.git
   git push -u origin main
   ```

   (Thay `<ten-tai-khoan>` và `<ten-repo>` bằng thông tin thật của bạn. GitHub sẽ hỏi đăng nhập — nếu dùng HTTPS, bạn cần tạo **Personal Access Token** thay cho mật khẩu, xem hướng dẫn tại `github.com/settings/tokens`.)

### Cách B — Upload trực tiếp qua trình duyệt (không cần cài Git)

1. Tạo repo mới trên GitHub như bước 1 ở trên.
2. Trong trang repo vừa tạo, bấm **uploading an existing file** (hoặc **Add file → Upload files**).
3. Kéo thả **toàn bộ nội dung bên trong** thư mục `betaratio-website` (không kéo cả thư mục cha) vào khung upload — bao gồm cả các thư mục con `css/`, `js/`, `images/`, `industries/`, `products/`.
4. Cuộn xuống, bấm **Commit changes**.

> Lưu ý: GitHub web upload không giữ được cấu trúc thư mục nếu bạn kéo cả thư mục `betaratio-website` — hãy mở thư mục ra và kéo các file/thư mục con bên trong.

## 4. Bật GitHub Pages (để có link website công khai)

1. Vào repo trên GitHub → tab **Settings** → mục **Pages** (menu bên trái).
2. Ở **Source**, chọn nhánh `main`, thư mục `/ (root)` → bấm **Save**.
3. Sau 1–2 phút, GitHub sẽ cấp link dạng:
   `https://<ten-tai-khoan>.github.io/<ten-repo>/`
4. (Tùy chọn) Nếu có domain riêng (vd. `betaratio.com`), thêm file `CNAME` chứa domain đó vào repo và cấu hình DNS trỏ về GitHub Pages theo [hướng dẫn chính thức](https://docs.github.com/vi/pages/configuring-a-custom-domain-for-your-github-pages-site).

## 5. Việc cần làm trước khi vận hành chính thức (checklist)

Site hiện dùng dữ liệu và thông tin liên hệ **mẫu** — cần cập nhật trước khi công khai với khách hàng thật:

- [ ] Thay số điện thoại, email, địa chỉ thật trong `build.py` (đầu file, các biến `PHONE`, `EMAIL`, `ADDRESS`) rồi chạy lại `python3 build.py`, **hoặc** tìm–thay trực tiếp trong các file `.html` nếu không dùng Python.
- [ ] Thay `SITE_DOMAIN_PLACEHOLDER` trong `build.py` (hoặc trực tiếp trong `robots.txt`, `sitemap.xml`, thẻ `<link rel="canonical">` mỗi trang) bằng domain thật.
- [ ] Kết nối form "Yêu cầu báo giá" (`contact.html`) với dịch vụ nhận email thật — ví dụ [Formspree](https://formspree.io), Google Forms, hoặc API backend riêng. Hiện tại form chỉ hiển thị thông báo xác nhận trên trình duyệt (xem `js/main.js`, phần `data-rfq-form`) và **chưa gửi dữ liệu đi đâu cả**.
- [ ] Thay ảnh minh họa/placeholder (icon, khối gradient) bằng ảnh thật: sản phẩm, nhà máy, dây chuyền sản xuất.
- [ ] Nhúng Google Maps thật vào khung bản đồ ở `contact.html` (tìm dòng `<span class="cap">Bản đồ vị trí...`).
- [ ] Xác minh lại số liệu trong mục "Case Studies" (trang chủ và `resources.html`) bằng dữ liệu dự án thật đã được khách hàng đồng ý công bố.
- [ ] Tải file catalogue/datasheet PDF thật lên và cập nhật liên kết ở `resources.html` (hiện đang là liên kết `#` giữ chỗ).
- [ ] Đính kèm bản sao chứng chỉ ISO 9001:2015 / FDA / QCVN thật (nếu muốn cho tải trực tiếp).

## 6. Sửa nội dung sau này

- Với thay đổi nhỏ (sửa câu chữ, giá, thông tin liên hệ): sửa trực tiếp trong file `.html` tương ứng bằng bất kỳ trình soạn thảo nào (VS Code, Notepad++...).
- Với thay đổi lặp lại trên nhiều trang (vd. đổi toàn bộ menu, thêm ngành công nghiệp mới, sửa số điện thoại ở mọi trang): sửa dữ liệu trong `build.py` rồi chạy `python3 build.py` để sinh lại toàn bộ trang — cách này nhanh và tránh sai sót khi phải sửa tay hàng chục file.

---

Website được thiết kế dựa trên tài liệu kiến trúc thông tin nội bộ Betaratio — dữ liệu sản phẩm/ngành lấy từ bản thiết kế gốc, hình ảnh là minh họa và cần được thay thế bằng ảnh thật trước khi vận hành chính thức.
