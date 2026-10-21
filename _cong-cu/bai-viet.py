# -*- coding: utf-8 -*-
# Người tạo: Quang Mai Phú – Quan Construction
# Nội dung các bài viết hướng dẫn (SEO) – mỗi bài là 1 trang tĩnh /tin-tuc/<slug>.html
# Định dạng thân bài: danh sách khối ("h2", text) | ("p", html) | ("ul", [html,...]) | ("ol", [html,...]) | ("note", html)
# Liên kết điều luật: dùng hàm L(id, dieu, chữ hiển thị) -> /phap-ly/<id>.html#d<dieu>


def L(i, d, t):
    return f'<a href="/phap-ly/{i}.html#d{d}">{t}</a>'


BAI = [
    {
        "slug": "thu-tuc-xin-giay-phep-xay-dung-nha-o-rieng-le-2026",
        "date": "2026-10-21",
        "title": "Thủ tục xin giấy phép xây dựng nhà ở riêng lẻ 2026: hồ sơ, nơi nộp, thời hạn",
        "desc": "Hướng dẫn xin giấy phép xây dựng nhà ở riêng lẻ năm 2026 theo Luật Xây dựng 2025 và Nghị định 217/2026/NĐ-CP: hồ sơ gồm gì, nộp ở đâu, bao lâu có giấy phép.",
        "summary": "Hồ sơ, nơi nộp và thời hạn cấp giấy phép xây dựng nhà ở riêng lẻ theo Luật Xây dựng 2025 và Nghị định 217/2026/NĐ-CP.",
        "body": [
            ("p", "Từ ngày 01/07/2026, việc cấp giấy phép xây dựng (GPXD) thực hiện theo Luật Xây dựng số 135/2025/QH15 và Nghị định 217/2026/NĐ-CP. Bài viết tóm tắt những điểm chủ nhà cần biết khi xin phép xây nhà ở riêng lẻ, kèm liên kết tới đúng điều luật để anh chị đọc nguyên văn."),
            ("h2", "1. Nhà ở riêng lẻ có phải xin giấy phép không?"),
            ("p", "Theo " + L("135-2025-qh15", "43", "Điều 43 Luật Xây dựng 2025") + ", trước khi khởi công, chủ đầu tư phải có giấy phép xây dựng, trừ một số trường hợp được miễn. Với nhà ở, trường hợp miễn phổ biến nhất là nhà ở riêng lẻ <b>dưới 7 tầng, tổng diện tích sàn dưới 500 m²</b> và <b>không nằm trong</b> các khu vực đã có quy hoạch như khu phát triển đô thị, khu dân cư nông thôn theo quy hoạch chung, khu vực xây dựng theo quy hoạch chung xã hoặc khu vực đã có quy chế quản lý kiến trúc."),
            ("p", "Phần lớn nhà ở tại phường, thị trấn và khu dân cư đã có quy hoạch vẫn <b>phải xin phép</b>. Xem chi tiết các trường hợp được miễn tại bài " + '<a href="/tin-tuc/nha-o-rieng-le-nao-duoc-mien-giay-phep-xay-dung.html">Nhà ở riêng lẻ nào được miễn giấy phép xây dựng?</a>'),
            ("h2", "2. Hồ sơ xin giấy phép xây dựng nhà ở riêng lẻ"),
            ("p", "Theo " + L("217-2026-nd-cp", "60", "Điều 60 Nghị định 217/2026/NĐ-CP") + ", hồ sơ của hộ gia đình, cá nhân gồm:"),
            ("ol", [
                "Đơn đề nghị cấp giấy phép xây dựng theo Mẫu số 01 Phụ lục II Nghị định 217/2026/NĐ-CP.",
                "Một trong các giấy tờ hợp pháp về đất đai theo " + L("217-2026-nd-cp", "55", "Điều 55") + " (sổ đỏ, sổ hồng, giấy tờ đủ điều kiện cấp Giấy chứng nhận…).",
                "Bộ bản vẽ thiết kế: mặt bằng công trình trên lô đất kèm sơ đồ vị trí; mặt bằng các tầng, mặt đứng, mặt cắt chính; mặt bằng và mặt cắt móng kèm sơ đồ đấu nối cấp nước, thoát nước, cấp điện.",
                "Bản cam kết bảo đảm an toàn đối với công trình liền kề.",
                "Kết quả thủ tục phòng cháy chữa cháy, báo cáo thẩm tra thiết kế (chỉ khi pháp luật yêu cầu).",
            ]),
            ("h2", "3. Ai được tự thiết kế nhà?"),
            ("p", "Theo " + L("207-2026-nd-cp", "10", "Điều 10 Nghị định 207/2026/NĐ-CP") + ", chủ nhà được <b>tự tổ chức thiết kế</b> nếu nhà đồng thời: dưới 3 tầng, không có tầng hầm, tổng diện tích sàn dưới 250 m² và cao dưới 12 m. Nhà lớn hơn phải do tổ chức, cá nhân có chuyên môn, kinh nghiệm thiết kế; nhà từ 7 tầng hoặc từ 2 tầng hầm trở lên còn phải tuân thủ quy chuẩn phòng cháy chữa cháy."),
            ("h2", "4. Nộp hồ sơ ở đâu?"),
            ("p", "Theo " + L("217-2026-nd-cp", "53", "Điều 53 Nghị định 217/2026/NĐ-CP") + ", <b>Ủy ban nhân dân cấp xã (xã, phường)</b> nơi có công trình cấp giấy phép xây dựng cho nhà ở riêng lẻ của hộ gia đình, cá nhân."),
            ("p", "Theo " + L("217-2026-nd-cp", "54", "Điều 54") + ", hồ sơ được nộp <b>trực tuyến trên Cổng Dịch vụ công quốc gia</b>; chỉ khi có sự cố không thể nộp trực tuyến mới nộp trực tiếp tại Bộ phận Một cửa hoặc qua bưu chính công ích."),
            ("h2", "5. Bao lâu có giấy phép?"),
            ("ul", [
                "Nhà ở riêng lẻ: <b>07 ngày làm việc</b> kể từ ngày nhận đủ hồ sơ hợp lệ (cấp mới, điều chỉnh, sửa chữa, cải tạo, di dời, có thời hạn).",
                "Gia hạn hoặc cấp lại giấy phép: 05 ngày làm việc.",
                "Nếu hồ sơ thiếu, cơ quan cấp phép thông báo <b>một lần</b> bằng thư điện tử hoặc tin nhắn; chủ nhà có 02 ngày làm việc để bổ sung.",
            ]),
            ("h2", "6. Xây không phép, sai phép bị xử lý thế nào?"),
            ("p", "Từ 26/08/2026, hành vi vi phạm trật tự xây dựng bị xử phạt theo " + L("339-2026-nd-cp", "25", "Điều 25 Nghị định 339/2026/NĐ-CP") + ". Ngoài phạt tiền, công trình có thể bị buộc dừng thi công để làm thủ tục cấp phép hoặc buộc tháo dỡ phần sai phép, đồng thời ảnh hưởng tới việc hoàn công và đăng ký nhà vào sổ đỏ sau này."),
            ("note", "Bài viết chỉ tóm tắt để tham khảo, không thay thế văn bản pháp luật. Một số tỉnh có quy định riêng về quy hoạch, kiến trúc; nên kiểm tra thông tin quy hoạch tại UBND xã, phường trước khi thiết kế."),
        ],
    },
    {
        "slug": "nha-o-rieng-le-nao-duoc-mien-giay-phep-xay-dung",
        "date": "2026-10-21",
        "title": "Nhà ở riêng lẻ nào được miễn giấy phép xây dựng? (Luật Xây dựng 2025)",
        "desc": "Các trường hợp nhà ở riêng lẻ được miễn giấy phép xây dựng theo Điều 43 Luật Xây dựng 2025: điều kiện về số tầng, diện tích sàn, khu vực quy hoạch và sửa chữa cải tạo.",
        "summary": "Điều kiện để nhà ở riêng lẻ được miễn giấy phép xây dựng theo Điều 43 Luật Xây dựng 2025 và những lưu ý khi xây nhà không cần phép.",
        "body": [
            ("p", "Nhiều chủ nhà ở nông thôn thắc mắc nhà mình có phải xin giấy phép xây dựng không. Câu trả lời nằm ở " + L("135-2025-qh15", "43", "khoản 2 Điều 43 Luật Xây dựng 2025") + " (có hiệu lực từ 01/07/2026)."),
            ("h2", "1. Nhà ở riêng lẻ được miễn giấy phép khi nào?"),
            ("p", "Theo điểm g khoản 2 Điều 43, được miễn giấy phép đối với công trình cấp IV, công trình nhà ở riêng lẻ <b>dưới 07 tầng</b> và có <b>tổng diện tích sàn xây dựng dưới 500 m²</b>, đồng thời <b>không thuộc</b> một trong các khu vực sau:"),
            ("ul", [
                "Khu chức năng, khu vực phát triển đô thị được xác định trong quy hoạch chung thành phố;",
                "Khu chức năng, khu dân cư nông thôn, khu vực phát triển đô thị trong quy hoạch chung đô thị thuộc tỉnh, thuộc thành phố, quy hoạch chung khu kinh tế, khu du lịch quốc gia;",
                "Khu vực xây dựng được xác định trong quy hoạch chung xã;",
                "Khu vực đã có quy chế quản lý kiến trúc.",
            ]),
            ("p", "Nói cách khác, nhà nhỏ ở khu vực <b>chưa có quy hoạch</b> nêu trên mới được miễn. Nhà nằm trong khu dân cư theo quy hoạch chung xã hoặc trong đô thị vẫn phải xin phép dù chỉ 1–2 tầng."),
            ("h2", "2. Sửa chữa, cải tạo nhà có cần xin phép?"),
            ("p", "Theo điểm h khoản 2 Điều 43, được miễn giấy phép khi sửa chữa, cải tạo <b>bên trong</b> công trình, hoặc sửa chữa mặt ngoài không tiếp giáp đường trong đô thị có yêu cầu quản lý kiến trúc; với điều kiện không thay đổi mục đích, công năng sử dụng, không ảnh hưởng an toàn kết cấu chịu lực và bảo đảm phòng cháy chữa cháy, môi trường."),
            ("h2", "3. Được miễn phép vẫn phải tuân thủ gì?"),
            ("ul", [
                "Vẫn phải phù hợp mục đích sử dụng đất và quy hoạch được duyệt (nếu có).",
                "Thiết kế, thi công phải tuân thủ tiêu chuẩn, quy chuẩn và bảo đảm an toàn cho công trình lân cận theo " + L("207-2026-nd-cp", "10", "Điều 10 Nghị định 207/2026/NĐ-CP") + ".",
                "Muốn được chứng nhận quyền sở hữu nhà vào sổ đỏ, chủ nhà chuẩn bị giấy tờ theo " + L("31-2024-qh15", "148", "Điều 148 Luật Đất đai") + "; trường hợp phải xin phép thì giấy phép xây dựng là giấy tờ quan trọng nhất.",
            ]),
            ("p", "Khi không chắc nhà mình thuộc khu vực nào, nên hỏi bộ phận địa chính – xây dựng của UBND xã, phường hoặc xin thông tin quy hoạch theo " + L("47-2024-qh15", "55", "Điều 55 Luật Quy hoạch đô thị và nông thôn") + " trước khi khởi công."),
            ("note", "Bài viết chỉ tóm tắt để tham khảo. Xem toàn văn quy định tại " + L("135-2025-qh15", "43", "Điều 43 Luật Xây dựng 2025") + "."),
        ],
    },
    {
        "slug": "hoan-cong-va-dang-ky-nha-vao-so-do-2026",
        "date": "2026-10-21",
        "title": "Hoàn công nhà ở và đăng ký nhà vào sổ đỏ năm 2026: giấy tờ, trình tự, thời gian",
        "desc": "Xây xong nhà cần làm gì để được ghi nhà vào sổ đỏ? Giấy tờ, trình tự đăng ký tài sản gắn liền với đất theo Luật Đất đai 2024, Nghị định 101/2024 và Nghị định 207/2026.",
        "summary": "Xây xong nhà cần chuẩn bị giấy tờ gì để hoàn công và đăng ký quyền sở hữu nhà vào Giấy chứng nhận (sổ đỏ) theo quy định mới.",
        "body": [
            ("p", "\"Hoàn công\" là cách gọi quen thuộc của việc hoàn tất thủ tục sau khi xây nhà để được <b>ghi nhận quyền sở hữu nhà ở trên Giấy chứng nhận</b> (sổ đỏ, sổ hồng). Pháp luật hiện hành gọi đây là đăng ký tài sản gắn liền với đất."),
            ("h2", "1. Trong lúc xây: giữ lại hồ sơ"),
            ("p", "Theo " + L("207-2026-nd-cp", "10", "Điều 10 Nghị định 207/2026/NĐ-CP") + ", chủ nhà tự tổ chức thi công, giám sát và chịu trách nhiệm an toàn; pháp luật <b>khuyến khích</b> chủ nhà lập và lưu trữ hồ sơ công trình. Nên giữ: giấy phép xây dựng, bản vẽ được duyệt, hợp đồng thi công, biên bản nghiệm thu, hóa đơn vật tư chính. Với nhà từ 7 tầng hoặc từ 2 tầng hầm trở lên, việc thi công, giám sát phải theo đầy đủ quy định của Nghị định 207/2026."),
            ("h2", "2. Giấy tờ chứng minh quyền sở hữu nhà"),
            ("p", "Theo " + L("31-2024-qh15", "148", "Điều 148 Luật Đất đai 2024") + ", hộ gia đình, cá nhân được chứng nhận quyền sở hữu nhà ở khi có một trong các giấy tờ, trong đó phổ biến nhất là <b>giấy phép xây dựng nhà ở</b> (với trường hợp phải xin phép). Các giấy tờ khác gồm hợp đồng mua bán, tặng cho, thừa kế nhà ở hợp lệ, bản án, quyết định của Tòa án…"),
            ("h2", "3. Hồ sơ và trình tự đăng ký"),
            ("ul", [
                "Nếu đất <b>đã có sổ đỏ</b>: làm thủ tục đăng ký biến động để bổ sung nhà vào Giấy chứng nhận. Hồ sơ theo " + L("101-2024-nd-cp", "29", "Điều 29 Nghị định 101/2024/NĐ-CP") + ": đơn đăng ký biến động (Mẫu số 11/ĐK), Giấy chứng nhận đã cấp, giấy tờ về tài sản (giấy phép xây dựng…).",
                "Nếu <b>chưa có sổ</b>: đăng ký đất đai và tài sản lần đầu, hồ sơ theo " + L("101-2024-nd-cp", "28", "Điều 28") + ", trình tự theo " + L("101-2024-nd-cp", "31", "Điều 31") + " và " + L("101-2024-nd-cp", "36", "Điều 36 Nghị định 101/2024/NĐ-CP") + ".",
            ]),
            ("h2", "4. Mất bao lâu?"),
            ("p", "Theo " + L("101-2024-nd-cp", "22", "Điều 22 Nghị định 101/2024/NĐ-CP") + ": đăng ký đất đai, tài sản lần đầu không quá <b>20 ngày làm việc</b>, cấp Giấy chứng nhận lần đầu không quá 03 ngày làm việc; các trường hợp đăng ký biến động có thời gian riêng theo từng loại tại cùng điều này."),
            ("h2", "5. Những trường hợp hay vướng"),
            ("ul", [
                "Xây không phép hoặc sai phép ở khu vực phải xin phép: phải xử lý vi phạm theo " + L("339-2026-nd-cp", "25", "Điều 25 Nghị định 339/2026/NĐ-CP") + " trước, có thể không được chứng nhận phần sai phép.",
                "Nhà xây trên đất chưa phải đất ở: phải chuyển mục đích sử dụng đất theo " + L("31-2024-qh15", "121", "Điều 121 Luật Đất đai") + ".",
                "Các trường hợp không được cấp Giấy chứng nhận: xem " + L("31-2024-qh15", "151", "Điều 151 Luật Đất đai") + ".",
            ]),
            ("note", "Bài viết chỉ tóm tắt để tham khảo, không thay thế văn bản pháp luật và hướng dẫn của Văn phòng đăng ký đất đai nơi có nhà."),
        ],
    },
    {
        "slug": "le-phi-truoc-ba-nha-dat-2026",
        "date": "2026-10-21",
        "title": "Lệ phí trước bạ nhà đất 2026: mức thu 0,5%, cách tính và trường hợp được miễn",
        "desc": "Lệ phí trước bạ nhà đất năm 2026: mức thu 0,5%, giá tính theo bảng giá đất và giá nhà của UBND tỉnh, các trường hợp được miễn khi tặng cho, thừa kế trong gia đình.",
        "summary": "Mức thu lệ phí trước bạ nhà đất 0,5%, cách tính theo bảng giá của UBND tỉnh và các trường hợp được miễn khi tặng cho, thừa kế trong gia đình.",
        "body": [
            ("p", "Khi đăng ký quyền sử dụng đất, quyền sở hữu nhà (mua bán, tặng cho, thừa kế, đăng ký nhà mới xây…), người đăng ký phải nộp lệ phí trước bạ, trừ trường hợp được miễn. Quy định hiện hành nằm ở Nghị định 10/2022/NĐ-CP và các nghị định sửa đổi, được hợp nhất tại " + L("33-vbhn-btc", "8", "Văn bản hợp nhất 33/VBHN-BTC") + "."),
            ("h2", "1. Mức thu"),
            ("p", "Theo " + L("33-vbhn-btc", "8", "Điều 8") + ": <b>nhà, đất có mức thu lệ phí trước bạ là 0,5%</b>."),
            ("h2", "2. Giá tính lệ phí trước bạ"),
            ("ul", [
                "<b>Đất:</b> giá đất tại Bảng giá đất do UBND tỉnh, thành phố ban hành, tại thời điểm kê khai (" + L("33-vbhn-btc", "7", "Điều 7") + ").",
                "<b>Nhà:</b> giá do UBND tỉnh, thành phố ban hành theo pháp luật về xây dựng, tại thời điểm kê khai.",
                "Một số trường hợp đặc biệt (mua đấu giá, nhà chung cư, nhà thuộc sở hữu nhà nước…) có cách tính riêng tại cùng Điều 7.",
            ]),
            ("p", "Công thức tham khảo: <b>Lệ phí = Diện tích × Đơn giá theo bảng giá của UBND tỉnh × 0,5%</b>. Ví dụ: thửa đất 100 m², bảng giá 5.000.000 đ/m² thì lệ phí đất = 100 × 5.000.000 × 0,5% = 2.500.000 đồng (chưa gồm phần nhà, nếu có)."),
            ("h2", "3. Trường hợp được miễn thường gặp"),
            ("p", "Theo " + L("33-vbhn-btc", "10", "Điều 10") + ", được miễn lệ phí trước bạ đối với nhà, đất nhận thừa kế hoặc quà tặng giữa: vợ với chồng; cha mẹ đẻ với con đẻ; cha mẹ nuôi với con nuôi; cha mẹ chồng với con dâu; cha mẹ vợ với con rể; ông bà nội, ngoại với cháu nội, ngoại; anh chị em ruột với nhau. Ngoài ra còn một số trường hợp khác như phân chia tài sản chung của hộ gia đình, tài sản hợp nhất của vợ chồng…"),
            ("h2", "4. Lưu ý về văn bản mới"),
            ("p", "Nghị định " + L("202-2026-nd-cp", "1", "202/2026/NĐ-CP") + " sửa đổi Nghị định 10/2022/NĐ-CP sẽ có hiệu lực từ <b>01/03/2027</b>. Khi giao dịch từ thời điểm đó, cần kiểm tra lại quy định mới."),
            ("note", "Bài viết chỉ để tham khảo. Số tiền chính xác do cơ quan thuế thông báo khi kê khai; bảng giá đất, giá nhà khác nhau theo từng tỉnh."),
        ],
    },
]
