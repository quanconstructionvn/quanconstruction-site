# Người tạo: Quang Mai Phú – kiểm tra bản tiếng Anh Sổ tay xây dựng (so cấu trúc, liên kết với bản tiếng Việt)
# Dùng (ở thư mục gốc): python3 _cong-cu/kiem-so-tay-en.py [slug ...]
import json, os, re, sys, glob, importlib.util
D = os.path.dirname(os.path.abspath(__file__))
EN = os.path.join(D, "so-tay-en")
_s = importlib.util.spec_from_file_location("st", os.path.join(D, "so-tay-xay-dung.py")); _c = importlib.util.module_from_spec(_s); _s.loader.exec_module(_c)
DAU = re.compile(r"[ăâđêôơưáàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ]", re.I)
hrefs = lambda x: sorted(re.findall(r'href="([^"]+)"', json.dumps(x, ensure_ascii=False).replace('\\"', '"')))
loi = 0


def bao(ten, err):
    global loi
    if err: loi += 1; print("LỖI", ten, "; ".join(err))


def so_khoi(e, v, err):
    if [b[0] for b in e] != [b[0] for b in v]: err.append("số/loại khối khác bản Việt"); return
    for i, (a, b) in enumerate(zip(e, v)):
        k = b[0]
        if k in ("ul", "ol", "faq") and len(a[1]) != len(b[1]): err.append(f"khối {i}: số mục khác")
        if k == "table":
            if len(a[1]["cot"]) != len(b[1]["cot"]) or len(a[1]["dong"]) != len(b[1]["dong"]) or any(len(x) != len(y) for x, y in zip(a[1]["dong"], b[1]["dong"])):
                err.append(f"khối {i}: bảng khác số cột/dòng")
        if k == "st" and a[1] != b[1]: err.append(f"khối {i}: khối st phải giữ nguyên")
        if k == "html" and (a[1].count("<script") != b[1].count("<script") or re.findall(r'id="([^"]+)"', a[1]) != re.findall(r'id="([^"]+)"', b[1])):
            err.append(f"khối {i}: html khác số script/id")


vi = {t["slug"]: t for t in _c.TRANG}
slugs = sys.argv[1:] or [os.path.basename(f)[:-5] for f in glob.glob(EN + "/trang/*.json")]
for s in slugs:
    err = []
    try: e = json.load(open(os.path.join(EN, "trang", s + ".json"), encoding="utf-8"))
    except Exception as ex: bao(s, [str(ex)]); continue
    v = vi.get(s)
    if not v: bao(s, ["không có trang tiếng Việt"]); continue
    if set(e) != {"title", "ngan", "desc", "summary", "lead", "body"}: err.append(f"khóa sai {sorted(e)}")
    vb = v["body"]
    if s == "bieu-mau":  # nhóm bảng biểu mẫu do chương trình dựng
        i = next(j for j, (k, x) in enumerate(vb) if k == "h2"); j = next(j for j, (k, x) in enumerate(vb) if k == "h2" and x.startswith("Mẫu đang chờ"))
        vb = vb[:i] + [["bieu-mau", "groups"]] + vb[j:]
        if "{N}" not in json.dumps(e["body"][0], ensure_ascii=False): err.append("đoạn đầu thiếu {N}")
    so_khoi(e.get("body", []), vb, err)
    vh = hrefs(vb)
    if hrefs(e.get("body", [])) != vh: err.append("liên kết href khác bản Việt")
    if len(e.get("desc", "")) > 170: err.append(f"desc dài {len(e['desc'])}")
    n = len(DAU.findall(re.sub(r"<[^>]+>", " ", json.dumps(e, ensure_ascii=False))))
    if n > 80: err.append(f"còn {n} ký tự có dấu tiếng Việt")
    bao(s, err)
print(f"Đã kiểm {len(slugs)} trang, {loi} trang lỗi")
