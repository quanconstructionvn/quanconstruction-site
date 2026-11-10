# SEO tự động cho Quan Construction
Người tạo: Quang Mai Phú

Mục tiêu: mỗi lần CMS hoặc mã nguồn thay đổi, tạo trang HTML cho tin có nội dung đầy đủ, danh sách tin đọc được không cần JavaScript và sitemap theo trang công khai thực tế. Phát triển đồng thời xây nhà trọn gói và dự toán–bóc khối lượng.

Chọn build bằng Python tiêu chuẩn và xuất bản bằng GitHub Actions/Pages; giữ JSON làm nguồn CMS, giữ nguyên bài HTML cũ nếu không có body CMS. Không chạy công cụ cũ ghi đè danh sách tin. Phương án ghi ngược file sinh ra vào main gây xung đột với CMS và vòng lặp triển khai nên không chọn.

Không đổi DNS, không hứa thứ hạng, không tạo bài hoặc giá giả. Nội dung CMS dạng văn bản thuần được escape, đường dẫn bài bị giới hạn trong /tin-tuc/. Sitemap loại trang quản trị và noindex, dùng ngày commit thực thay vì ngày chạy. Bản build không chứa công cụ nội bộ, git và tests.

Triển khai cần chọn Settings → Pages → Source: GitHub Actions. Chuẩn bị nhánh và PR để kiểm tra trước khi tích hợp.
