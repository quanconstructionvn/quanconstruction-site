# -*- coding: utf-8 -*-
# Người tạo: Quang Mai Phú – Quan Construction
# Ghi lịch đăng bài (đã đăng / hẹn đăng) ra _cong-cu/lich-dang.md.
# GitHub Actions (.github/workflows/giu-lich-dang.yml) chạy mỗi tháng và commit file này,
# vừa để anh xem nhanh lịch, vừa giữ kho có cập nhật (GitHub tắt lịch chạy nếu kho 60 ngày không đổi).
import os, importlib.util
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sp = importlib.util.spec_from_file_location("bv", os.path.join(ROOT, "_cong-cu", "bai-viet.py"))
bv = importlib.util.module_from_spec(sp); sp.loader.exec_module(bv)
hom_nay = datetime.now(timezone(timedelta(hours=7))).strftime("%Y-%m-%d")
fmt = lambda d: "/".join(reversed(d.split("-")))
bai = sorted(bv.BAI, key=lambda b: b["date"])
da = [b for b in bai if b["date"] <= hom_nay]
cho = [b for b in bai if b["date"] > hom_nay]
dong = [f"# Lịch đăng bài viết – cập nhật {fmt(hom_nay)}",
        "<!-- Người tạo: Quang Mai Phú. File tạo tự động bởi _cong-cu/lich-dang.py, không sửa tay. -->", "",
        f"Đã đăng: {len(da)} bài · Hẹn đăng: {len(cho)} bài" + (f" (bài cuối {fmt(cho[-1]['date'])})" if cho else ""), "",
        "## Sắp đăng", ""] + [f"- {fmt(b['date'])} – [{b['title']}](/tin-tuc/{b['slug']}.html)" for b in cho] + [
        "", "## Đã đăng (mới nhất trước)", ""] + [f"- {fmt(b['date'])} – [{b['title']}](/tin-tuc/{b['slug']}.html)" for b in reversed(da)]
if not cho:
    dong[3] += " – HẾT BÀI HẸN ĐĂNG, cần soạn thêm"
open(os.path.join(ROOT, "_cong-cu", "lich-dang.md"), "w", encoding="utf-8").write("\n".join(dong) + "\n")
print(dong[3])
