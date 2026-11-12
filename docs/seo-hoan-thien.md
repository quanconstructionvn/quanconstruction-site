# Hoàn thiện khả năng tìm thấy nội dung website
Người tạo/chỉnh sửa: Quang Mai Phú — ngày 12/11/2026.

## Mục tiêu
Hoàn tất phần website có thể kiểm soát để Google tìm và đánh giá toàn bộ trang công khai; không tuyên bố ép Google lập chỉ mục hoặc bảo đảm đề xuất/tăng hạng.

## Căn cứ kiểm tra
Báo cáo hoàn tất từ workflow 43145448243: 160 URL, 57 đã lập chỉ mục; 51 Google chưa xác định URL, 50 đã phát hiện nhưng chưa lập chỉ mục, 2 đã thu thập nhưng chưa lập chỉ mục. Các URL chưa được lập chỉ mục phân bố ở trang dự toán, nội dung mới, thư viện pháp lý và bản tiếng Anh. Không phát hiện lỗi HTTP, noindex hoặc canonical trong phạm vi kiểm tra đó. Đây là ảnh chụp trạng thái tại thời điểm kiểm tra, không phải dữ liệu thời gian thực.

## Thay đổi
- Tạo `/so-do-trang.html` tự động từ toàn bộ canonical công khai thực tế, chia nhóm dịch vụ/công ty, hướng dẫn, sổ tay, pháp lý và tiếng Anh.
- Liên kết danh mục và hai dịch vụ từ chân các trang công khai. Kiểm tra build bảo đảm mọi URL trong sitemap XML đều có liên kết HTML truy cập được.
- Không đưa trang nội bộ, noindex, URL ngoài website, alias canonical hoặc bài chưa đến ngày xuất bản vào danh mục.
- Hoàn thành hai bài ngày 12/11/2026 về kiểm tra chi phí xây nhà trọn gói và hồ sơ thuê dự toán/BOQ; có tên người tạo và liên kết đến dịch vụ tương ứng. Không dùng giá, dự án, hình ảnh hoặc chứng nhận chưa xác nhận. Ví dụ BOQ ghi rõ là minh họa.
- Bỏ giới hạn địa danh trong tiêu đề/mô tả trang xây nhà và mô tả dịch vụ; giữ nguyên địa chỉ văn phòng thực tế.
- Sửa tạo danh sách tin: giữ bài CMS và các bài HTML ngoài bộ bài tự sinh, không xóa mọi đường dẫn `/tin-tuc/`. Nội dung CMS ưu tiên khi cùng URL với bài tự sinh.
- Giữ lịch kiểm tra hằng ngày 08:00 giờ Việt Nam và cơ chế thử lại API; không tự yêu cầu lập chỉ mục bằng API sai mục đích.

## Xác minh
Chạy toàn bộ unittest, tạo bài theo lịch ngày Việt Nam, tạo trang pháp lý rồi build site. Kiểm tra canonical, mô tả, JSON-LD, H1, sitemap và liên kết nội bộ. Lặp build để kiểm tra ổn định. Triển khai qua GitHub Pages và xác minh các URL mới từ website thực tế.

## Giới hạn và vận hành
HTTP tốt và có liên kết không bảo đảm Google chọn lập chỉ mục. Không sửa nguyên văn luật chỉ để tạo nội dung khác. Không bịa đánh giá khách hàng hoặc công trình. Google có thể chọn không lập chỉ mục những nội dung trùng lặp/ít giá trị theo đánh giá của họ; cần dùng các báo cáo sau triển khai để đánh giá tiếp.
Nội dung mới vẫn cần người có chuyên môn kiểm chứng trước khi công bố. Không có tác vụ tự sáng tác bài, gửi liên hệ hoặc quản lý Google Business Profile trong thay đổi này. Báo cáo Google là tự động hằng ngày, không phải người trợ lý theo dõi liên tục giữa các lượt trò chuyện.
