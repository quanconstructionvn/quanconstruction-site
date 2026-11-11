/* Người tạo: Quang Mai Phú – Quan Construction
   Công cụ tương tác cho Sổ tay xây dựng: bản đồ công việc, checklist hồ sơ, thuật ngữ.
   Dữ liệu nằm trong <script type="application/json" data-st="..."> trên từng trang; trạng thái người dùng lưu trên trình duyệt (localStorage). */
(function () {
  'use strict';
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  var csv = function (rows, name) {
    var t = '﻿' + rows.map(function (r) { return r.map(function (c) { c = String(c == null ? '' : c).replace(/<[^>]+>/g, '').replace(/"/g, '""'); return '"' + c + '"'; }).join(','); }).join('\r\n');
    var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([t], { type: 'text/csv;charset=utf-8' })); a.download = name; document.body.appendChild(a); a.click(); a.remove();
  };
  var css = document.createElement('style');
  css.textContent = '.st-bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 14px}.st-bar select,.st-bar input{font:inherit;padding:8px 10px;border:1px solid #c9d4e6;border-radius:8px;background:#fff}' +
    '.st-btn{font:inherit;font-weight:700;padding:8px 14px;border-radius:8px;border:1px solid var(--navy,#0a1d3f);background:#fff;color:var(--navy,#0a1d3f);cursor:pointer}.st-btn.p{background:var(--navy,#0a1d3f);color:#fff}' +
    '.st-prog{height:8px;background:#e6ecf5;border-radius:6px;overflow:hidden;margin:6px 0 14px}.st-prog i{display:block;height:100%;background:#2e7d32}' +
    '.st-gd{margin:18px 0 6px;font-size:13px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--blue,#1d4fa3)}' +
    '.st-card{border:1px solid var(--line,#dfe6f1);border-radius:12px;margin:0 0 10px;background:#fff}.st-card>summary{cursor:pointer;padding:12px 14px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}' +
    '.st-card>summary b{flex:1 1 260px;color:var(--navy,#0a1d3f)}.st-tag{font-size:12px;border-radius:6px;padding:2px 8px;background:#eef3fb;color:#26406b;font-weight:700}' +
    '.st-tag.s1{background:#fff4d6;color:#8a5a00}.st-tag.s2{background:#fde2e1;color:#b3261e}.st-tag.s3{background:#e3f4e5;color:#1e6b23}.st-tag.s4{background:#eceff3;color:#666}' +
    '.st-body{padding:0 14px 14px}.st-body h4{margin:12px 0 6px;font-size:14.5px;color:var(--navy,#0a1d3f)}.st-body label.ck{display:flex!important;flex-direction:row!important;justify-content:flex-start!important;gap:8px;align-items:flex-start;margin:0 0 6px;text-align:left!important;font-weight:400!important}.st-body label.ck input{width:auto!important;flex:0 0 auto;margin:5px 0 0}.st-body label.ck span{flex:1 1 auto}.st-q label input{width:auto!important}.st-bar label{display:inline-flex!important;flex-direction:row!important;align-items:center;gap:6px}' +
    '.st-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:8px;margin:8px 0}.st-row label{font-size:13px;font-weight:700;display:flex;flex-direction:column;gap:3px}.st-row input,.st-row select{font:inherit;font-weight:400;padding:7px 9px;border:1px solid #c9d4e6;border-radius:8px}' +
    '.st-ck td{vertical-align:top}.st-ck select{font:inherit;padding:4px 6px;border:1px solid #c9d4e6;border-radius:6px}.st-ck input[type=text]{font:inherit;width:100%;padding:4px 6px;border:1px solid #c9d4e6;border-radius:6px}' +
    '.st-q{border:1px solid var(--line,#dfe6f1);border-radius:12px;padding:12px 14px;margin:0 0 10px;background:#fff}.st-q p{margin:0 0 8px;font-weight:700}.st-q label{display:block;padding:6px 8px;border-radius:8px;cursor:pointer;margin:0 0 4px}' +
    '.st-q label:hover{background:#f4f7fc}.st-q label.ok{background:#e3f4e5}.st-q label.sai{background:#fde2e1}.st-q .gt{display:none;font-size:14.5px;background:#f4f7fc;border-radius:8px;padding:8px 10px;margin-top:6px}.st-q.xong .gt{display:block}' +
    '.st-kq{position:sticky;bottom:10px;background:var(--navy,#0a1d3f);color:#fff;border-radius:12px;padding:12px 16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap;z-index:5}' +
    '.st-gl dt{font-weight:800;color:var(--navy,#0a1d3f);margin-top:10px}.st-gl dd{margin:2px 0 0}.st-gl .en{color:var(--blue,#1d4fa3)}' +
    '@media print{.st-bar,.st-kq,.cs-nav,header,footer,.cs-toc{display:none!important}.st-card{break-inside:avoid}.st-card>.st-body{display:block!important}}';
  document.head.appendChild(css);

  function data(el) { try { return JSON.parse(el.textContent); } catch (e) { return null; } }

  /* ---------- 1. Bản đồ công việc ---------- */
  function banDo(el, D) {
    var K = 'st-bando-v1', S = store.get(K, {}), host = document.createElement('div'); el.after(host);
    var TT = [['', 'Chưa thực hiện'], ['1', 'Đang thực hiện'], ['2', 'Đang vướng'], ['3', 'Đã hoàn thành'], ['4', 'Không áp dụng']];
    host.innerHTML = '<div class="st-bar"><label>Loại dự án <select data-f="loai"><option value="">Tất cả</option>' + D.loai.map(function (x) { return '<option value="' + x[0] + '">' + esc(x[1]) + '</option>'; }).join('') + '</select></label>' +
      '<label>Giai đoạn <select data-f="gd"><option value="">Tất cả</option>' + D.giai_doan.map(function (x) { return '<option value="' + x[0] + '">' + esc(x[1]) + '</option>'; }).join('') + '</select></label>' +
      '<input type="search" data-f="q" placeholder="Tìm công việc, hồ sơ…"><button class="st-btn" data-a="csv">Xuất Excel (CSV)</button><button class="st-btn" data-a="in">In</button><button class="st-btn" data-a="xoa">Xóa dữ liệu đã lưu</button></div>' +
      '<div data-tong></div><div data-ds></div>';
    var f = { loai: (S._f || {}).loai || '', gd: '', q: '' };
    host.querySelector('[data-f=loai]').value = f.loai;
    function st(id) { return S[id] || (S[id] = { tt: '', ng: '', han: '', ck: {} }); }
    function save() { store.set(K, S); }
    function ve() {
      var ds = D.viec.filter(function (v) { return (!f.loai || v.ap_dung.indexOf(f.loai) >= 0) && (!f.gd || v.gd === f.gd) && (!f.q || (v.ten + ' ' + v.buoc.join(' ') + ' ' + (v.ho_so || []).join(' ')).toLowerCase().indexOf(f.q) >= 0); });
      var xong = ds.filter(function (v) { return st(v.id).tt === '3' || st(v.id).tt === '4'; }).length;
      host.querySelector('[data-tong]').innerHTML = '<b>' + xong + '/' + ds.length + '</b> công việc đã xong hoặc không áp dụng' + (ds.some(function (v) { return st(v.id).tt === '2'; }) ? ' · <span class="st-tag s2">có việc đang vướng</span>' : '') + '<div class="st-prog"><i style="width:' + (ds.length ? 100 * xong / ds.length : 0) + '%"></i></div>';
      var out = '';
      D.giai_doan.forEach(function (g) {
        var vg = ds.filter(function (v) { return v.gd === g[0]; }); if (!vg.length) return;
        out += '<div class="st-gd">' + esc(g[1]) + '</div>';
        vg.forEach(function (v) {
          var s = st(v.id), n = v.buoc.filter(function (b, i) { return s.ck[i]; }).length;
          out += '<details class="st-card" data-id="' + v.id + '"' + (s._mo ? ' open' : '') + '><summary><b>' + esc(v.ten) + '</b><span class="st-tag s' + (s.tt || '0') + '">' + esc(TT.filter(function (t) { return t[0] === s.tt; })[0][1]) + '</span><span class="st-tag">' + n + '/' + v.buoc.length + ' bước</span>' + (s.han ? '<span class="st-tag">hạn ' + esc(s.han) + '</span>' : '') + '</summary><div class="st-body">' +
            (v.mo_ta ? '<p>' + v.mo_ta + '</p>' : '') +
            '<div class="st-row"><label>Trạng thái<select data-k="tt">' + TT.map(function (t) { return '<option value="' + t[0] + '"' + (t[0] === s.tt ? ' selected' : '') + '>' + t[1] + '</option>'; }).join('') + '</select></label>' +
            '<label>Người phụ trách<input data-k="ng" value="' + esc(s.ng) + '"></label><label>Hạn hoàn thành<input type="date" data-k="han" value="' + esc(s.han) + '"></label></div>' +
            '<h4>01 · Làm theo trình tự</h4>' + v.buoc.map(function (b, i) { return '<label class="ck"><input type="checkbox" data-ck="' + i + '"' + (s.ck[i] ? ' checked' : '') + '><span>' + b + '</span></label>'; }).join('') +
            (v.ho_so && v.ho_so.length ? '<h4>02 · Hồ sơ cần có</h4><ul>' + v.ho_so.map(function (h) { return '<li>' + h + '</li>'; }).join('') + '</ul>' : '') +
            (v.lien_ket && v.lien_ket.length ? '<h4>03 · Biểu mẫu, hướng dẫn</h4><ul>' + v.lien_ket.map(function (h) { return '<li>' + h + '</li>'; }).join('') + '</ul>' : '') +
            (v.can_cu && v.can_cu.length ? '<h4>04 · Quy định ở đâu?</h4><ul>' + v.can_cu.map(function (h) { return '<li>' + h + '</li>'; }).join('') + '</ul>' : '') +
            (v.luu_y ? '<p class="cs-note" style="margin:10px 0 0">' + v.luu_y + '</p>' : '') + '</div></details>';
        });
      });
      host.querySelector('[data-ds]').innerHTML = out || '<p>Không có công việc phù hợp bộ lọc.</p>';
    }
    host.addEventListener('change', function (e) {
      var t = e.target, c = t.closest('[data-id]');
      if (t.dataset.f) { f[t.dataset.f] = t.value; S._f = { loai: f.loai }; save(); ve(); return; }
      if (!c) return; var s = st(c.dataset.id);
      if (t.dataset.k) s[t.dataset.k] = t.value; if (t.dataset.ck) s.ck[t.dataset.ck] = t.checked;
      save(); var mo = c.open; ve(); var n = host.querySelector('[data-id="' + c.dataset.id + '"]'); if (n && mo) n.open = true;
    });
    host.addEventListener('input', function (e) { if (e.target.dataset.f === 'q') { f.q = e.target.value.toLowerCase(); ve(); } });
    host.addEventListener('toggle', function (e) { var c = e.target; if (c.dataset && c.dataset.id) { st(c.dataset.id)._mo = c.open; save(); } }, true);
    host.addEventListener('click', function (e) {
      var a = e.target.dataset.a; if (!a) return;
      if (a === 'in') { host.querySelectorAll('details').forEach(function (d) { d.open = true; }); window.print(); }
      if (a === 'xoa' && confirm('Xóa toàn bộ trạng thái đã lưu trên máy này?')) { S = {}; save(); ve(); }
      if (a === 'csv') csv([['Giai đoạn', 'Công việc', 'Trạng thái', 'Người phụ trách', 'Hạn', 'Bước đã xong']].concat(D.viec.map(function (v) {
        var s = st(v.id); return [D.giai_doan.filter(function (g) { return g[0] === v.gd; })[0][1], v.ten, TT.filter(function (t) { return t[0] === s.tt; })[0][1], s.ng, s.han, v.buoc.filter(function (b, i) { return s.ck[i]; }).length + '/' + v.buoc.length];
      })), 'ban-do-cong-viec.csv');
    });
    ve();
  }

  /* ---------- 2. Checklist hồ sơ ---------- */
  function checklist(el, D) {
    var K = 'st-ck-' + (D.ma || 'ho-so'), S = store.get(K, {}), host = document.createElement('div'); el.after(host);
    var OPT = [['', '—'], ['co', 'Có'], ['thieu', 'Thiếu'], ['kad', 'Không áp dụng']];
    host.innerHTML = '<div class="st-bar"><input type="search" data-q placeholder="Tìm hồ sơ…"><label><input type="checkbox" data-thieu> Chỉ hiện hồ sơ thiếu/chưa đánh dấu</label><button class="st-btn" data-a="csv">Xuất Excel (CSV)</button><button class="st-btn" data-a="in">In</button><button class="st-btn" data-a="xoa">Xóa đánh dấu</button></div><div data-tong></div><div data-ds></div>';
    var q = '', thieu = false;
    function ve() {
      var tong = 0, co = 0, out = '', stt = 0;
      D.nhom.forEach(function (g, gi) {
        var rows = '';
        g.muc.forEach(function (m, mi) {
          var id = gi + '.' + mi, s = S[id] || {}; tong++; stt++; if (s.v === 'co' || s.v === 'kad') co++;
          if (q && (m.ten + ' ' + (m.don_vi || '')).toLowerCase().indexOf(q) < 0) return;
          if (thieu && (s.v === 'co' || s.v === 'kad')) return;
          rows += '<tr data-id="' + id + '"><td>' + stt + '</td><td>' + m.ten + (m.can_cu ? '<br><small>' + m.can_cu + '</small>' : '') + '</td><td>' + esc(m.don_vi || '') + '</td><td><select>' + OPT.map(function (o) { return '<option value="' + o[0] + '"' + (o[0] === (s.v || '') ? ' selected' : '') + '>' + o[1] + '</option>'; }).join('') + '</select></td><td><input type="text" value="' + esc(s.gc || '') + '" placeholder="Ghi chú"></td></tr>';
        });
        if (rows) out += '<h3>' + esc(g.ten) + '</h3><div class="cs-tbl st-ck"><table><thead><tr><th>STT</th><th>Hồ sơ</th><th>Đơn vị lập</th><th>Tình trạng</th><th>Ghi chú</th></tr></thead><tbody>' + rows + '</tbody></table></div>';
      });
      host.querySelector('[data-tong]').innerHTML = '<b>' + co + '/' + tong + '</b> hồ sơ đã có hoặc không áp dụng<div class="st-prog"><i style="width:' + (tong ? 100 * co / tong : 0) + '%"></i></div>';
      host.querySelector('[data-ds]').innerHTML = out || '<p>Không có hồ sơ phù hợp.</p>';
    }
    host.addEventListener('change', function (e) {
      var tr = e.target.closest('tr[data-id]');
      if (e.target.matches('[data-thieu]')) { thieu = e.target.checked; ve(); return; }
      if (!tr) return; var s = S[tr.dataset.id] || (S[tr.dataset.id] = {});
      if (e.target.tagName === 'SELECT') s.v = e.target.value; else s.gc = e.target.value; store.set(K, S); if (e.target.tagName === 'SELECT') ve();
    });
    host.addEventListener('input', function (e) { if (e.target.matches('[data-q]')) { q = e.target.value.toLowerCase(); ve(); } });
    host.addEventListener('click', function (e) {
      var a = e.target.dataset.a; if (!a) return;
      if (a === 'in') window.print();
      if (a === 'xoa' && confirm('Xóa toàn bộ đánh dấu trên máy này?')) { S = {}; store.set(K, S); ve(); }
      if (a === 'csv') { var rows = [['STT', 'Nhóm', 'Hồ sơ', 'Đơn vị lập', 'Căn cứ', 'Tình trạng', 'Ghi chú']], n = 0;
        D.nhom.forEach(function (g, gi) { g.muc.forEach(function (m, mi) { var s = S[gi + '.' + mi] || {}; n++; rows.push([n, g.ten, m.ten, m.don_vi, m.can_cu, (OPT.filter(function (o) { return o[0] === (s.v || ''); })[0] || OPT[0])[1], s.gc]); }); });
        csv(rows, (D.ma || 'checklist') + '.csv'); }
    });
    ve();
  }

  /* ---------- 4. Thuật ngữ ---------- */
  function thuatNgu(el, D) {
    var host = document.createElement('div'); el.after(host);
    var nhom = D.reduce(function (a, t) { if (a.indexOf(t.nhom) < 0) a.push(t.nhom); return a; }, []);
    host.innerHTML = '<div class="st-bar"><input type="search" data-q placeholder="Tìm tiếng Anh hoặc tiếng Việt…" style="flex:1 1 260px"><select data-n><option value="">Mọi nhóm</option>' + nhom.map(function (n) { return '<option>' + esc(n) + '</option>'; }).join('') + '</select><span data-dem></span></div><dl class="st-gl" data-ds></dl>';
    var q = '', n = '';
    function ve() {
      var ds = D.filter(function (t) { return (!n || t.nhom === n) && (!q || (t.en + ' ' + t.vi + ' ' + (t.viet_tat || '')).toLowerCase().indexOf(q) >= 0); });
      host.querySelector('[data-dem]').textContent = ds.length + ' thuật ngữ';
      host.querySelector('[data-ds]').innerHTML = ds.map(function (t) { return '<dt><span class="en">' + esc(t.en) + (t.viet_tat ? ' (' + esc(t.viet_tat) + ')' : '') + '</span> – ' + esc(t.vi) + '</dt><dd>' + t.dn + '</dd>'; }).join('');
    }
    host.addEventListener('input', function (e) { if (e.target.matches('[data-q]')) { q = e.target.value.toLowerCase(); ve(); } });
    host.addEventListener('change', function (e) { if (e.target.matches('[data-n]')) { n = e.target.value; ve(); } });
    ve();
  }

  var MAP = { 'ban-do': banDo, 'checklist': checklist, 'thuat-ngu': thuatNgu };
  document.querySelectorAll('script[type="application/json"][data-st]').forEach(function (el) { var d = data(el), fn = MAP[el.dataset.st]; if (d && fn) fn(el, d); });
})();
