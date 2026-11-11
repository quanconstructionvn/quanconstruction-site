# Bàn giao – Sổ tay xây dựng (nhánh mới của website quanconstruction.biz.vn)

Người tạo: Quang Mai Phú – Quan Construction. Cập nhật: 11/11/2026.

## 1. Mục tiêu (anh Phú yêu cầu)
- Làm một nhánh trang chuyên sâu cho dân xây dựng & văn phòng (QA/QC, QS, CCM, giám sát), **làm tương tự qlda.gxd.vn**, công khai, miễn phí.
- Tên nhánh: **Sổ tay xây dựng** (đã đổi từ "Chuyên sâu"). Đường dẫn: `/so-tay-xay-dung.html`, trang con `/so-tay-xay-dung/<slug>.html`.
- Biểu mẫu: **chỉ lấy từ luật**, không tự biên; mỗi mẫu 3 bản **PDF, Word, Excel**. Giấy tờ luật không ban hành mẫu thì trình bày theo đúng nội dung bắt buộc của điều luật, ghi rõ trên mẫu.
- **Chưa đăng web.** Anh chọn: đợi xong **Đợt 1** rồi đăng một lần. Chỉ push `main` khi anh trả lời đồng ý.

## 2. Trạng thái hiện tại
- Toàn bộ nằm trên nhánh git **`nhap/chuyen-sau`** (repo `quanconstructionvn/quanconstruction-site`). Đã push nhánh này, CHƯA gộp vào `main`.
- Đã có: 12 trang (sổ tay trình tự dự án, hồ sơ – thủ tục, QA/QC, giám sát, QS, CCM, lập dự toán, định mức – đơn giá – chỉ số giá, hồ sơ chất lượng & nghiệm thu, biểu mẫu, hỏi đáp 40 câu, công cụ tính nhanh 7 công cụ); menu "Sổ tay xây dựng" trên mọi trang; 24 biểu mẫu × 3 định dạng.
- Đợt 1 (anh duyệt làm **tất cả**): **đã gộp vào nhánh `nhap/chuyen-sau`** (dữ liệu trong `_cong-cu/so-tay-du-lieu/`, nạp bởi hàm `_dot_1()` cuối `_cong-cu/so-tay-xay-dung.py`), **đang chờ anh duyệt đăng**:
  1. Bản đồ công việc tương tác (21 công việc, 5 giai đoạn, lọc loại dự án, checklist, trạng thái, người phụ trách, hạn, lưu trình duyệt, xuất CSV, in).
  2. Checklist hồ sơ khi thanh tra, kiểm tra (182 mục, 10 nhóm; có/thiếu/không áp dụng, ghi chú, xuất CSV, in).
  3. Hỏi đáp mở rộng: +50 câu chi phí – dự toán – định mức – giá, +43 câu thẩm định/GPXD, hợp đồng – thanh quyết toán, chất lượng – PCCC, năng lực – xử phạt (tổng ~133).
  4. Trắc nghiệm ôn tập: 5 đề × 25 câu (QLDA đề 1, 2; pháp luật xây dựng đề 1; giám sát thi công đề 1; định giá xây dựng đề 1).
  5. Thuật ngữ Anh – Việt QLDA (~150–200 thuật ngữ, tìm kiếm, lọc nhóm).

## 3. Cấu trúc mã (trong repo)
| File | Vai trò |
|---|---|
| `_cong-cu/so-tay-xay-dung.py` | Dữ liệu các trang (TRANG, NHOM, VAI_TRO…). Trang Biểu mẫu tự dựng từ `_cong-cu/bieu-mau-danh-sach.json` (hàm `_bieu_mau()` cuối file). |
| `_cong-cu/tao-so-tay-xay-dung.py` | Tạo `/so-tay-xay-dung.html` + trang con + cập nhật sitemap. Khối nội dung: h2, h3, p, ul, ol, note, table, faq, html, st (công cụ tương tác). |
| `_cong-cu/bieu-mau/*.json` | Mô tả từng biểu mẫu (chép nguyên văn từ phụ lục văn bản). |
| `_cong-cu/tao-bieu-mau.py` | Tạo `.docx`, `.xlsx`, `.pdf` (LibreOffice) vào `so-tay-xay-dung/bieu-mau/` và `_cong-cu/bieu-mau-danh-sach.json`. Bảng > 8 cột tự chuyển khổ ngang. |
| `_cong-cu/so-tay-du-lieu/*.json` | Dữ liệu công cụ tương tác (bản đồ công việc, checklist, đề trắc nghiệm, thuật ngữ). |
| `js/so-tay-tuong-tac.js` | Engine tương tác: `ban-do`, `checklist`, `trac-nghiem`, `thuat-ngu` (đọc `<script type="application/json" data-st="…">`). |
| `_cong-cu/mau-trang-van-ban.html` | Khung trang dùng chung (đã thêm menu "Sổ tay xây dựng"). |

Lệnh tạo lại (chạy ở thư mục gốc repo): `python3 _cong-cu/tao-bieu-mau.py && python3 _cong-cu/tao-so-tay-xay-dung.py && python3 _cong-cu/tao-bai-viet.py && python3 _cong-cu/tao-trang-phap-ly.py`. Kiểm tra: `python3 -m unittest discover -s tests`, `python3 _cong-cu/build_site.py --output _site`, `python3 _cong-cu/check_seo_build.py _site`. Không commit `_cong-cu/__pycache__`.

## 4. Quy tắc nội dung (bắt buộc giữ)
- Pháp lý chỉ dựa toàn văn thư viện `phap-ly/van-ban/<id>.json` + `phap-ly/danh-muc.json`; dẫn điều bằng `L(id, dieu, chữ)`; không suy diễn, không bịa số.
- Không nêu thẩm quyền "cấp huyện" (thư viện chưa có NĐ 151/2025 phân định chính quyền 2 cấp).
- Phân biệt quy định chỉ bắt buộc với dự án vốn đầu tư công/vốn nhà nước/PPP (NĐ 210, 206, 193, mức bảo hành 3%/5%…).
- NĐ 347/2026 (15/09/2026) đã bãi bỏ Điều 10 NĐ 105/2025: chủ đầu tư tự nghiệm thu PCCC, khai báo CSDL PCCC.
- Luật 24/2026/QH16 sửa khoản 1, 2 Điều 88 Luật Xây dựng từ 01/03/2027. QCVN 01:2026 hiệu lực 01/01/2027. TT 64/2025 (giảm 50% phí) hết áp dụng sau 31/12/2026.
- Bộ luật Dân sự id `91-2015-qh13`. Không đăng toàn văn TCVN (bản quyền). Không chép chữ của GXD – chỉ học cách tổ chức.
- Trắc nghiệm ghi rõ: đề ôn tập do Quan Construction soạn, không phải đề thi chính thức.

## 5. Dữ liệu Đợt 1 (nếu phiên mới không còn thư mục tạm)
Dữ liệu đã được chép vào repo tại `_cong-cu/so-tay-du-lieu/` (khi gộp xong). Nếu bị mất, soạn lại theo mục 2 và schema trong `js/so-tay-tuong-tac.js`:
- ban-do: `{loai:[[ma,ten]], giai_doan:[[ma,ten]], viec:[{id,gd,ten,ap_dung[],mo_ta,buoc[],ho_so[],lien_ket[],can_cu[],luu_y}]}`
- checklist: `{ma, nhom:[{ten, muc:[{ten,don_vi,can_cu}]}]}`
- trac-nghiem: `{cau:[{q,a[4],dung,loai:'pl'|'cm',giai_thich}], dat:{diem,sai_pl}|null}`
- thuat-ngu: `[{en,vi,viet_tat,nhom,dn}]`

## 6. Việc còn lại
1. Chờ anh duyệt. Khi anh trả lời "đăng": gộp `nhap/chuyen-sau` vào `main` (git merge --no-ff), push, kiểm tra GitHub Actions "SEO build and Pages deployment" thành công, mở thử https://quanconstruction.biz.vn/so-tay-xay-dung.html.
2. **Đợt 2** (cần nạp văn bản vào thư viện trước – Cổng PLQG chặn IP nước ngoài, phải dùng máy tính của anh hoặc anh tải PDF lên Project): Luật Đầu tư công 58/2024, Luật Đấu thầu sửa đổi + NĐ 214/2025, NĐ 254/2025 (mẫu thanh toán vốn ĐTC), NĐ 220/2026 (bảo hiểm), TTLT 11/2025 (lãng phí), QĐ 821/QĐ-KTNN, QĐ 1040/QĐ-BXD (mẫu hợp đồng), phụ lục NĐ 207/2026 và Phụ lục II NĐ 217/2026 (GPXD), Mẫu 09–17 PL I NĐ 217, Mẫu 10–12/QTDA TT 73. Sau đó làm: sổ tay vốn ĐTC/ngoài ĐTC, mục "Thanh tra, kiểm toán & bài học", các biểu mẫu còn thiếu.
3. **Đợt 3**: giáo trình định mức – đơn giá chuyên sâu; hướng dẫn phần mềm QC Quản lý dự án (ảnh giao diện có trong Project: `QC-Quan-ly-Du-an/anh-giao-dien/`).

## 7. Việc khác đang chạy (đã xong, chỉ để nhớ)
- 117 bài viết hẹn đăng tự động tới 27/12/2027 (`_cong-cu/bai-viet.py`, GitHub Actions `pages.yml` chạy 00:05 giờ VN; `giu-lich-dang.yml` ngày 1 và 15 giữ lịch không bị tắt).
- Việc định kỳ "Rà soát bài hẹn đăng hằng tháng" (ngày 15) và "Kiểm tra website hằng tuần" (thứ Hai).
- Các nhánh nháp cũ trên GitHub xóa không được do mạng ngắt – có thể xóa tay ở mục Branches.
