# Kiểm tra SEO và lập chỉ mục định kỳ
Người tạo: Quang Mai Phú

## Đã cấu hình
Workflow **Daily SEO and indexing audit** chạy 08:00 hằng ngày theo giờ Việt Nam (GitHub có thể xếp hàng trễ), hoặc chạy tay bằng Actions → chọn workflow → Run workflow → main.

Mỗi lượt đọc sitemap đang xuất bản, kiểm tra tối đa 200 URL với 4 kết nối đồng thời. Ưu tiên trang chủ và hai dịch vụ. Kiểm tra HTTP, chuyển hướng, noindex và canonical; giữ sitemap tự động từ luồng xuất bản hiện tại. Không tự gửi yêu cầu lập chỉ mục, không thay đổi nội dung hoặc dữ liệu Google.

Kết quả nằm trong Summary của lượt chạy và artifact **seo-audit-report**, gồm Markdown/JSON, lưu 30 ngày. Báo cáo không tự gửi email hoặc tạo issue. Nếu HTTP/canonical/noindex có vấn đề, job báo lỗi để chủ kho thấy trong Actions; cấu hình thông báo GitHub cá nhân quyết định có nhận email hay không.

**Chưa cấp quyền Search Console thì chỉ kiểm tra kỹ thuật.** HTTP 200 hoặc có trong sitemap không chứng minh URL đã được Google lập chỉ mục. Báo cáo ghi `not_checked`, không giả thành `not_indexed`. Lỗi quyền/hạn mức/API cũng không được tính thành URL chưa lập chỉ mục.

## Kết nối Search Console một lần
Việc này phải thực hiện bằng tài khoản có quyền quản lý Google Cloud, Search Console và secrets của repo. Không gửi khóa JSON vào chat và không commit khóa vào mã nguồn.

1. Trong Google Cloud, chọn/tạo project cho công ty và bật **Google Search Console API** (`searchconsole.googleapis.com`).
2. Tạo service account dành riêng cho kiểm tra SEO; không cần gán quyền Owner/Editor cho project. Tạo khóa JSON cho service account nếu chính sách công ty cho phép. Với tổ chức bắt buộc không dùng khóa, cần cấu hình Workload Identity Federation riêng thay cho bước này.
3. Trong Search Console, chọn property chính xác **https://quanconstruction.biz.vn/** → Settings → Users and permissions → Add user. Thêm email service account với quyền **Full** để dùng URL Inspection, không cấp Owner.
4. Trong repo GitHub → Settings → Secrets and variables → Actions → New repository secret. Tên **GSC_CREDENTIALS_JSON**, giá trị là toàn bộ nội dung file JSON. Không dùng Variables hoặc dán vào workflow. Chỉ người quản trị thực hiện bước lưu bí mật.
5. Chạy lại **Daily SEO and indexing audit**. Kết nối chỉ hoàn tất khi báo cáo ghi `connected` và có kết quả URL từ Google; nếu `permission_error`, kiểm tra đúng property, email service account và API đã bật.

Code dùng scope `https://www.googleapis.com/auth/webmasters.readonly`; chỉ gọi URL Inspection API. Khóa JSON có thể được dùng để đọc dữ liệu mà service account được cấp quyền, vì vậy cần bảo quản, giới hạn quyền và thu hồi khi không sử dụng. Không tạo/cấp quyền service account tự động trong mã này.

## Đọc kết quả
- `indexed`: Google trả verdict PASS.
- `not_indexed`: Google trả FAIL/NEUTRAL; đọc `coverage` để biết lý do, không coi tất cả là lỗi.
- `unknown`: Google chưa cung cấp kết quả rõ ràng.
- `not_checked`: chưa gọi được API hoặc nằm sau điểm kết nối/quota bị lỗi.
- `api_error`: không nhận được phản hồi hợp lệ cho URL đó.

Hiện website dưới 200 URL nên nằm trong một lượt. Khi vượt 200, báo cáo hiển thị rõ phần chưa được kiểm tra; cần tăng/phân lô phù hợp hạn mức API thay vì hiểu đây là báo cáo toàn bộ website.

Tài liệu chính thức:
- https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect
- https://support.google.com/webmasters/answer/7687615
