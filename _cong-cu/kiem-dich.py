# Người tạo: Quang Mai Phú – kiểm tra bản dịch tiếng Anh bài viết
# Dùng (ở thư mục gốc): python3 _cong-cu/kiem-dich.py [slug ...]   (không có slug = kiểm tất cả bản đã dịch)
import json, os, re, sys, glob, importlib.util
D = os.path.dirname(os.path.abspath(__file__))
EN = os.path.join(D, "bai-viet-en")
_s = importlib.util.spec_from_file_location("bv", os.path.join(D, "bai-viet.py")); _b = importlib.util.module_from_spec(_s); _s.loader.exec_module(_b)
vi = {b["slug"]: b for b in _b.BAI}
slugs = sys.argv[1:] or [os.path.basename(f)[:-5] for f in glob.glob(EN + "/*.json")]
DAU = re.compile(r"[ăâđêôơưáàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ]", re.I)
hrefs = lambda x: sorted(re.findall(r'href="([^"]+)"', json.dumps(x, ensure_ascii=False).replace('\\"', '"')))
loi = 0
for s in slugs:
    f = os.path.join(EN, s + ".json")
    err = []
    try:
        e = json.load(open(f, encoding="utf-8"))
    except Exception as ex:
        print("LỖI", s, ex); loi += 1; continue
    v = vi.get(s)
    if not v: err.append("không có bài tiếng Việt cùng slug")
    else:
        if set(e) != {"title", "desc", "summary", "body"}: err.append(f"khóa sai {sorted(e)}")
        if [b[0] for b in e.get("body", [])] != [b[0] for b in v["body"]]: err.append("số/loại khối khác bản Việt")
        else:
            for i, (a, b) in enumerate(zip(e["body"], v["body"])):
                if isinstance(b[1], list) and len(a[1]) != len(b[1]): err.append(f"khối {i}: số mục danh sách khác")
        if hrefs(e["body"]) != hrefs(v["body"]): err.append("liên kết href khác bản Việt")
        if len(e.get("desc", "")) > 175: err.append(f"desc dài {len(e['desc'])}")
        txt = re.sub(r"<[^>]+>", " ", json.dumps(e, ensure_ascii=False))
        n = len(DAU.findall(txt))
        if n > 60: err.append(f"còn {n} ký tự có dấu tiếng Việt")
    if err: loi += 1; print("LỖI", s, "; ".join(err))
print(f"Đã kiểm {len(slugs)} bài, {loi} bài lỗi")
