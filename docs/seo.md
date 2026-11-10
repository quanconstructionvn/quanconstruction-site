# SEO và xuất bản tự động
Người tạo: Quang Mai Phú

## Kích hoạt một lần
1. Tích hợp PR SEO vào main.
2. Vào Settings → Pages → Build and deployment → Source: **GitHub Actions**. Giữ nguyên tên miền riêng `quanconstruction.biz.vn`, kiểm tra Enforce HTTPS.
3. Vào Actions → SEO build and Pages deployment → Run workflow trên main. Xác nhận cả build và deploy thành công.
4. Trong Google Search Console của đúng website, gửi `https://quanconstruction.biz.vn/sitemap.xml` một lần. File xác minh Google hiện có được giữ trong bản triển khai. Có file xác minh không đồng nghĩa đã có quyền Search Console.

Sau đó mỗi lần main đổi (bao gồm lưu từ Decap CMS), workflow kiểm thử, build và triển khai lại. Không cần API key hay dịch vụ trả phí. Sitemap được tạo lại theo các trang công khai thực tế; không gửi yêu cầu lập chỉ mục tự động và không bảo đảm thời điểm Google lập chỉ mục/thứ hạng.

## Đăng bài từ /admin/
- Điền ngày `dd/mm/yyyy`, tiêu đề, tóm tắt, nội dung đầy đủ dạng văn bản thuần. Dòng trống tạo đoạn mới. HTML được hiển thị dạng chữ để tránh thực thi mã.
- Nên điền slug duy nhất, ví dụ `cach-doc-bang-boq`. Giữ slug sau khi xuất bản để ổn định URL. Bỏ trống thì slug được tạo từ tiêu đề.
- Với bài mới có nội dung: để trống Liên kết, hệ thống tạo `/tin-tuc/<slug>.html` và nối vào danh sách tin + sitemap trong bản triển khai.
- Bài HTML cũ với nội dung CMS rỗng được giữ nguyên. Muốn quản lý nội dung bài cũ qua CMS, điền body và giữ đúng link cũ. Không dùng cùng link cho hai mục.
- Chỉ đăng tin ngắn: để trống body, tin xuất hiện trong danh sách nhưng không sinh trang riêng.
- Xóa mục CMS sẽ xóa trang do build sinh ra ở lần triển khai kế tiếp; bài HTML lưu sẵn trong repo chỉ bị xóa khi xóa file nguồn.
- Bài CMS hiện chỉ sinh bản tiếng Việt. Các trang tiếng Anh và bài HTML hiện có vẫn được giữ.

## Nguồn và công cụ cũ
Workflow mới không chạy `tao-bai-viet.py` vì công cụ đó quản lý bộ bài hướng dẫn riêng và có thể thay danh sách `/tin-tuc/` trong JSON. Nếu dùng công cụ cũ thủ công, phải kiểm tra diff để không mất mục CMS. Công cụ mới không ghi ngược vào main nên không xung đột với Decap.

## Hai dịch vụ ưu tiên
- `/xay-nha-tron-goi.html`: nhà ở, thi công phần thô–hoàn thiện; mô tả vị trí văn phòng và tiếp nhận khảo sát theo công trình.
- `/du-toan-boc-khoi-luong.html`: BOQ, dự toán, thanh quyết toán, nhận hồ sơ từ xa.
- Không đăng đơn giá, thời gian thực hiện hoặc công trình chưa được xác nhận. Trang dịch vụ chứa Service JSON-LD, canonical, mô tả và đường dẫn liên hệ.

## Kiểm tra và quay lại
Chạy `python3 -m unittest discover -s tests -v`, `python3 _cong-cu/build_site.py`, `python3 _cong-cu/check_seo_build.py _site`.
Chạy `python3 -m http.server 8000 --directory _site` để xem trước. `_site` là output được tạo lại, không sửa tay/commit.
Nếu build thất bại, bản Pages thành công trước đó tiếp tục phục vụ. Khôi phục bằng revert commit gây lỗi rồi chạy lại workflow; không cần đổi DNS. Các mục robots Disallow chỉ hướng dẫn crawler, không thay cho đăng nhập.

## Đo lường
Search Console: theo dõi trang được lập chỉ mục, truy vấn, lượt hiển thị, lượt nhấp; tách hai trang dịch vụ để đánh giá. Chưa có kết nối Search Console trong thay đổi này.
