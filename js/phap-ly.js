/* Người tạo: Quang Mai Phú – Tra cứu pháp luật (Quan Construction)
   Cập nhật 19/10/2026 (Quang Mai Phú): giao diện mới – tìm kiếm, 3 thẻ lĩnh vực → nhóm → văn bản; hành trình từng bước; tất cả văn bản gọn
   Dữ liệu: phap-ly/danh-muc.json + phap-ly/van-ban/<id>.json (mỗi điều: [số điều, tiêu đề, nội dung, chương])
   Nguồn toàn văn: Cổng Pháp luật quốc gia (phapluat.gov.vn) · Thống kê: js/thong-ke.js (xem_van_ban, search) */
(function(){
"use strict";
var $=function(s,r){return(r||document).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
var esc=function(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]})};
var fold=function(s){return String(s||"").normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/đ/g,"d").replace(/Đ/g,"D").toLowerCase()};
var p2=function(n){return(n<10?"0":"")+n};
var d=new Date(),TODAY=d.getFullYear()+"-"+p2(d.getMonth()+1)+"-"+p2(d.getDate());
var fmt=function(x){return x?x.split("-").reverse().join("/"):"—"};
var GROUPS=[["A","Văn bản Luật nền tảng"],["B1","Quản lý hoạt động xây dựng"],["B2","Chi phí đầu tư xây dựng"],["B3","Hợp đồng xây dựng"],["B4","Chất lượng, thi công và bảo trì"],["B5","Vật liệu xây dựng"],["B6","Năng lực, hệ thống thông tin"],["B7","Thanh toán – quyết toán vốn đầu tư"],["C","Dân sự, thương mại, đấu thầu"],["D","Đất đai & sổ đỏ"],["E","Nhà ở & kinh doanh bất động sản"],["G","Công chứng, thuế & lệ phí nhà đất"],["H","Xử phạt vi phạm hành chính"],["F","Quy hoạch"],["I","Kiến trúc"],["J","Phòng cháy, chữa cháy & cứu nạn, cứu hộ"]];
var GM={};GROUPS.forEach(function(g){GM[g[0]]=g[1]});
var AREAS=[
 {id:"xd",ten:"Xây dựng",mo:"Luật Xây dựng, hợp đồng, chi phí, chất lượng, thanh toán – quyết toán",nhom:["A","B1","B2","B3","B4","B5","B6","B7","C"],ic:'<path d="M3 21h18M5 21V9l7-5 7 5v12"/><path d="M9 21v-6h6v6"/>'},
 {id:"nha",ten:"Nhà ở & đất đai",mo:"Sổ đỏ, nhà ở, mua bán, công chứng, thuế phí, xử phạt",nhom:["D","E","G","H"],ic:'<path d="M4 20V10l8-6 8 6v10z"/><path d="M9 13h6M9 16h6"/>'},
 {id:"kt",ten:"Quy hoạch, kiến trúc & PCCC",mo:"Quy hoạch, quy chuẩn, kiến trúc, phòng cháy chữa cháy",nhom:["F","I","J"],ic:'<path d="M12 3c2 3 5 4.5 5 9a5 5 0 0 1-10 0c0-2 1-3 2-4 0 2 1 3 2 3 0-3-1-5 1-8z"/>'}];
var AM={};AREAS.forEach(function(a){a.nhom.forEach(function(n){AM[n]=a.id})});
var JOURNEY=[{"t": "Mua đất & kiểm tra sổ đỏ", "m": "Kiểm tra điều kiện chuyển nhượng, công chứng hợp đồng, sang tên Giấy chứng nhận.", "l": [["31-2024-qh15", "45", "Luật Đất đai – Đ45: Điều kiện chuyển nhượng, tặng cho quyền sử dụng đất"], ["46-2024-qh15", "44", "Luật Công chứng – Đ44: Thẩm quyền công chứng giao dịch bất động sản"], ["101-2024-nd-cp", "29", "NĐ 101/2024 – Đ29: Hồ sơ đăng ký biến động (sang tên)"], ["101-2024-nd-cp", "37", "NĐ 101/2024 – Đ37: Thủ tục đăng ký biến động, cấp sổ"], ["31-2024-qh15", "121", "Luật Đất đai – Đ121: Chuyển mục đích sử dụng đất (lên thổ cư)"], ["103-2024-nd-cp", "8", "NĐ 103/2024 – Đ8: Tiền sử dụng đất khi chuyển mục đích"]]}, {"t": "Xem quy hoạch & xin giấy phép xây dựng", "m": "Tra thông tin quy hoạch, chuẩn bị hồ sơ và xin GPXD nhà ở riêng lẻ.", "l": [["47-2024-qh15", "55", "Luật Quy hoạch ĐT&NT – Đ55: Cung cấp thông tin quy hoạch"], ["135-2025-qh15", "43", "Luật Xây dựng 2025 – Đ43: Quy định chung về cấp GPXD"], ["135-2025-qh15", "44", "Luật Xây dựng 2025 – Đ44: Cấp giấy phép xây dựng"], ["217-2026-nd-cp", "50", "NĐ 217/2026 – Đ50: Điều kiện cấp GPXD mới"], ["217-2026-nd-cp", "55", "NĐ 217/2026 – Đ55: Giấy tờ hợp pháp về đất để cấp GPXD"], ["217-2026-nd-cp", "60", "NĐ 217/2026 – Đ60: Hồ sơ GPXD nhà ở riêng lẻ"], ["217-2026-nd-cp", "53", "NĐ 217/2026 – Đ53: Thẩm quyền cấp GPXD"], ["217-2026-nd-cp", "63", "NĐ 217/2026 – Đ63: Điều chỉnh, gia hạn GPXD"], ["40-2019-qh14", "21", "Luật Kiến trúc – Đ21: Điều kiện hành nghề kiến trúc (người thiết kế)"], ["55-2024-qh15", "17", "Luật PCCC – Đ17: Thẩm định thiết kế về PCCC"]]}, {"t": "Khởi công & thi công", "m": "Điều kiện khởi công, trách nhiệm chủ nhà và các lỗi hay bị xử phạt.", "l": [["135-2025-qh15", "48", "Luật Xây dựng 2025 – Đ48: Điều kiện khởi công"], ["135-2025-qh15", "46", "Luật Xây dựng 2025 – Đ46: Quyền, trách nhiệm người xin GPXD"], ["339-2026-nd-cp", "21", "NĐ 339/2026 – Đ21: Vi phạm về khởi công"], ["339-2026-nd-cp", "25", "NĐ 339/2026 – Đ25: Vi phạm trật tự xây dựng (sai phép, không phép)"], ["55-2024-qh15", "20", "Luật PCCC – Đ20: Phòng cháy đối với nhà ở"], ["55-2024-qh15", "21", "Luật PCCC – Đ21: Nhà ở kết hợp sản xuất, kinh doanh"]]}, {"t": "Nghiệm thu & hoàn công", "m": "Nghiệm thu hoàn thành, hồ sơ hoàn thành công trình, bàn giao đưa vào sử dụng.", "l": [["135-2025-qh15", "57", "Luật Xây dựng 2025 – Đ57: Nghiệm thu công trình"], ["207-2026-nd-cp", "24", "NĐ 207/2026 – Đ24: Nghiệm thu hoàn thành công trình"], ["207-2026-nd-cp", "28", "NĐ 207/2026 – Đ28: Hồ sơ hoàn thành công trình"], ["207-2026-nd-cp", "30", "NĐ 207/2026 – Đ30: Bàn giao công trình"], ["55-2024-qh15", "18", "Luật PCCC – Đ18: Nghiệm thu về PCCC"]]}, {"t": "Đăng ký nhà vào sổ đỏ", "m": "Đăng ký quyền sở hữu nhà ở (tài sản gắn liền với đất) trên Giấy chứng nhận.", "l": [["31-2024-qh15", "148", "Luật Đất đai – Đ148: Chứng nhận quyền sở hữu nhà ở"], ["31-2024-qh15", "135", "Luật Đất đai – Đ135: Nguyên tắc cấp Giấy chứng nhận"], ["31-2024-qh15", "137", "Luật Đất đai – Đ137: Cấp sổ khi có giấy tờ về quyền sử dụng đất"], ["31-2024-qh15", "151", "Luật Đất đai – Đ151: Trường hợp không cấp Giấy chứng nhận"], ["101-2024-nd-cp", "28", "NĐ 101/2024 – Đ28: Hồ sơ đăng ký lần đầu"], ["101-2024-nd-cp", "22", "NĐ 101/2024 – Đ22: Thời gian giải quyết thủ tục"]]}, {"t": "Mua bán, tặng cho – thuế & phí", "m": "Điều kiện giao dịch nhà ở, công chứng, thuế TNCN và lệ phí trước bạ.", "l": [["27-2023-qh15", "160", "Luật Nhà ở – Đ160: Điều kiện nhà ở tham gia giao dịch"], ["27-2023-qh15", "164", "Luật Nhà ở – Đ164: Công chứng hợp đồng về nhà ở"], ["29-2023-qh15", "24", "Luật KD BĐS – Đ24: Nhà ở hình thành trong tương lai"], ["109-2025-qh15", "14", "Luật Thuế TNCN – Đ14: Thuế chuyển nhượng bất động sản"], ["33-vbhn-btc", "7", "Lệ phí trước bạ – Đ7: Giá tính lệ phí"], ["33-vbhn-btc", "8", "Lệ phí trước bạ – Đ8: Mức thu (%)"]]}];
function dl(d){d=String(d==null?"":d);return /^\d+[a-zđ]?$/i.test(d)?"Điều "+d:(/^PL\s/.test(d)?"Phụ lục "+d.slice(3):(/^P\d+$/.test(d)?"Phần "+d.slice(1):"Mục "+d))}
var S={laws:[],byId:{},texts:{},tab:"lv",area:null,group:null,step:0,allQ:"",showOld:false};
function status(l){if(l.hieuLucTu&&TODAY<l.hieuLucTu)return"chua";if(l.hieuLucDen&&TODAY>=l.hieuLucDen)return"het";return"con"}
var STL={con:"Còn hiệu lực",het:"Hết hiệu lực",chua:"Chưa có hiệu lực"};
function name(l){return(l.loai||"")+" "+(l.soHieu||"")}
function toast(m){var t=$("#plToast");t.textContent=m;t.hidden=false;clearTimeout(toast.t);toast.t=setTimeout(function(){t.hidden=true},2400)}
function copy(t){var ok=function(){toast("Đã sao chép")};if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(ok,function(){fb()})}else fb();
  function fb(){var a=document.createElement("textarea");a.value=t;document.body.appendChild(a);a.select();try{document.execCommand("copy");ok()}catch(e){toast("Hãy bôi đen để sao chép")}a.remove()}}
var V=function(){return $("#plView")};
function live(l){return S.showOld||status(l)!=="het"}
function sortL(a,b){return(a.thuTu||99)-(b.thuTu||99)}

/* ---------- Tải danh mục ---------- */
fetch("phap-ly/danh-muc.json?t="+Math.floor(Date.now()/36e5)).then(function(r){return r.json()}).then(function(j){
  S.laws=j.vanBan;S.laws.forEach(function(l){S.byId[l.id]=l});
  $("#plUpd").textContent=fmt(j.capNhat);
  render();openFromUrl();
}).catch(function(){V().innerHTML='<div class="pl-empty"><b>Không tải được danh mục</b>Vui lòng tải lại trang.</div>'});

/* ---------- Điều hướng ---------- */
function setTab(t){S.tab=t;$$("#plTabs button").forEach(function(b){b.setAttribute("aria-selected",String(b.dataset.tab===t))});render()}
$$("#plTabs button").forEach(function(b){b.onclick=function(){$("#plQ").value="";if(b.dataset.tab==="lv"){S.area=null;S.group=null}setTab(b.dataset.tab)}});
function render(){var v=V();
  if(S.tab==="ht")return renderJourney(v);
  if(S.tab==="all")return renderAll(v);
  if(!S.area)return renderAreas(v);
  if(!S.group)return renderGroups(v);
  renderGroupDocs(v);
}
function crumb(parts){return'<div class="pl-crumb">'+parts.join(' <span>›</span> ')+'</div>'}
function renderAreas(v){
  v.innerHTML='<div class="pl-areas">'+AREAS.map(function(a){var n=S.laws.filter(function(l){return AM[l.nhom]===a.id&&live(l)}).length;
    return'<button type="button" class="pl-area" data-a="'+a.id+'"><span class="ic"><svg viewBox="0 0 24 24">'+a.ic+'</svg></span><b>'+esc(a.ten)+'</b><span>'+esc(a.mo)+'</span><small>'+n+' văn bản ›</small></button>'}).join("")+'</div>';
  $$(".pl-area",v).forEach(function(b){b.onclick=function(){S.area=b.dataset.a;S.group=null;render();scrollTop()}});
}
function areaOf(id){return AREAS.filter(function(a){return a.id===id})[0]}
function renderGroups(v){var a=areaOf(S.area);
  var gs=a.nhom.map(function(n){return[n,S.laws.filter(function(l){return l.nhom===n&&live(l)}).length]}).filter(function(x){return x[1]});
  v.innerHTML=crumb(['<button type="button" data-back="lv">Lĩnh vực</button>','<b>'+esc(a.ten)+'</b>'])+
    '<div class="pl-groups">'+gs.map(function(g){return'<button type="button" class="pl-group" data-g="'+g[0]+'">'+esc(GM[g[0]])+'<em>'+g[1]+' văn bản</em></button>'}).join("")+'</div>';
  $("[data-back]",v).onclick=function(){S.area=null;render()};
  $$(".pl-group",v).forEach(function(b){b.onclick=function(){S.group=b.dataset.g;render();scrollTop()}});
}
function renderGroupDocs(v){var a=areaOf(S.area);
  var xs=S.laws.filter(function(l){return l.nhom===S.group&&live(l)}).sort(sortL);
  v.innerHTML=crumb(['<button type="button" data-back="lv">Lĩnh vực</button>','<button type="button" data-back="area">'+esc(a.ten)+'</button>','<b>'+esc(GM[S.group])+'</b>'])+
    '<div class="pl-bar"><span class="c">'+xs.length+' văn bản</span>'+oldToggle()+'</div>'+docList(xs);
  $('[data-back="lv"]',v).onclick=function(){S.area=null;S.group=null;render()};
  $('[data-back="area"]',v).onclick=function(){S.group=null;render()};
  bindDocs(v);bindOld(v);
}
function oldToggle(){return'<label><input type="checkbox" class="pl-old"'+(S.showOld?" checked":"")+'> Hiện cả văn bản hết hiệu lực</label>'}
function bindOld(v){var c=$(".pl-old",v);if(c)c.onchange=function(){S.showOld=c.checked;render()}}
function docList(xs){if(!xs.length)return'<div class="pl-empty"><b>Không có văn bản phù hợp</b>Thử từ khóa khác hoặc bật “Hiện cả văn bản hết hiệu lực”.</div>';
  return'<div class="pl-docs">'+xs.map(function(l){var st=status(l);
    return'<div class="pl-doc"><div class="m"><div class="n">'+(l.soDieu>0?'<a href="phap-ly/'+esc(l.id)+'.html" data-read="'+esc(l.id)+'" style="color:inherit;text-decoration:none">'+esc(name(l))+'</a>':esc(name(l)))+(st!=="con"?' <span class="st '+st+'">'+STL[st]+'</span>':"")+'</div><div class="t">'+esc(l.ten)+'</div></div><div class="a">'+
      (l.soDieu>0?'<button type="button" class="rd" data-read="'+esc(l.id)+'">Đọc</button>':"")+(l.linkCong?'<a href="'+esc(l.linkCong)+'" target="_blank" rel="noopener" title="Mở bản gốc trên Cổng Pháp luật quốc gia">Bản gốc ↗</a>':"")+'</div></div>'}).join("")+'</div>'}
function bindDocs(v){$$("[data-read]",v).forEach(function(b){b.onclick=function(e){if(e.ctrlKey||e.metaKey)return;e.preventDefault();openDoc(b.dataset.read)}})}
function renderAll(v){
  v.innerHTML='<div class="pl-bar"><input type="search" id="plAllQ" placeholder="Lọc theo số hiệu hoặc tên văn bản, ví dụ 210/2026" value="'+esc(S.allQ)+'" aria-label="Lọc văn bản">'+oldToggle()+'</div><div id="plAllList"></div>';
  var draw=function(){var q=fold(S.allQ.trim());var xs=S.laws.filter(function(l){return live(l)&&(!q||fold(name(l)+" "+l.ten).indexOf(q)>=0)});
    xs.sort(function(a,b){var ga=GROUPS.findIndex(function(g){return g[0]===a.nhom}),gb=GROUPS.findIndex(function(g){return g[0]===b.nhom});return ga-gb||sortL(a,b)});
    $("#plAllList").innerHTML='<p class="pl-bar"><span class="c">'+xs.length+' văn bản</span></p>'+docList(xs);bindDocs($("#plAllList"))};
  draw();$("#plAllQ").oninput=function(){S.allQ=this.value;draw()};bindOld(v);
}
function renderJourney(v){var s=JOURNEY[S.step];
  v.innerHTML='<div class="pl-steps" role="list">'+JOURNEY.map(function(x,i){return'<button type="button" data-s="'+i+'"'+(i===S.step?' aria-current="step"':"")+'><i>'+(i+1)+'</i>'+esc(x.t)+'</button>'}).join("")+'</div>'+
   '<div class="pl-step"><h3>Bước '+(S.step+1)+'. '+esc(s.t)+'</h3><p>'+esc(s.m)+'</p><ul>'+s.l.map(function(x){var p=x[2].split(" – ");var ten=p.length>1?p.slice(1).join(" – "):x[2];var src=p.length>1?p[0]:"";
     return'<li><a href="phap-ly/'+esc(x[0])+'.html#d'+esc(String(x[1]).replace(/\s+/g,'-'))+'" data-vb="'+esc(x[0])+'" data-dieu="'+esc(x[1])+'"><b>'+esc(src)+'</b><span>'+esc(ten)+'</span></a></li>'}).join("")+'</ul>'+
   '<div class="pl-nav"><button type="button" data-go="-1"'+(S.step?"":" disabled")+'>← Bước trước</button><button type="button" class="p" data-go="1"'+(S.step<JOURNEY.length-1?"":" disabled")+'>Bước tiếp theo →</button></div></div>';
  $$("[data-s]",v).forEach(function(b){b.onclick=function(){S.step=+b.dataset.s;render()}});
  $$("[data-go]",v).forEach(function(b){b.onclick=function(){S.step+= +b.dataset.go;render()}});
  $$("a[data-vb]",v).forEach(function(a){a.onclick=function(e){if(!S.byId[a.dataset.vb])return;e.preventDefault();openDoc(a.dataset.vb,a.dataset.dieu)}});
  var cur=$('[aria-current="step"]',v);if(cur&&cur.scrollIntoView)cur.scrollIntoView({block:"nearest",inline:"center"});
}
function scrollTop(){var t=$("#plTabs");if(t&&t.getBoundingClientRect().top<0)t.scrollIntoView({behavior:"smooth"})}

/* ---------- Toàn văn ---------- */
function loadText(id){if(S.texts[id])return Promise.resolve(S.texts[id]);
  return fetch("phap-ly/van-ban/"+encodeURIComponent(id)+".json").then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(a){
    var arts=a.map(function(x){return{dieu:x[0],tieuDe:x[1],noiDung:x[2],chuong:x[3],lawId:id,_f:fold(x[1]+" "+x[2]),_t:fold(x[1])}});S.texts[id]=arts;return arts})}
var cur=null;
function openDoc(id,dieu){var l=S.byId[id];if(!l)return;
  if(window.qcTk)qcTk("xem_van_ban",{van_ban:name(l),dieu:dieu?String(dieu):"",nhom:l.nhom});
  $("#rdT").textContent=name(l);$("#rdS").textContent=l.ten+" · Hiệu lực "+fmt(l.hieuLucTu)+(l.hieuLucDen?" → "+fmt(l.hieuLucDen):"");
  var lk=$("#rdLink");if(l.linkCong){lk.href=l.linkCong;lk.hidden=false}else lk.hidden=true;
  $("#rdTx").innerHTML='<div class="pl-load"><span class="spin"></span>Đang tải toàn văn…</div>';$("#rdToc").innerHTML="";
  $("#rdOv").hidden=false;document.body.style.overflow="hidden";
  loadText(id).then(function(arts){cur={l:l,arts:arts};
    var ch="",toc='<input type="search" id="rdF" placeholder="Lọc theo tên điều…" aria-label="Lọc điều">',tx="";
    arts.forEach(function(a){if(a.chuong&&a.chuong!==ch){ch=a.chuong;toc+='<div class="ch">'+esc(ch.split(" – ")[0])+'</div>';tx+='<div class="chp">'+esc(ch)+'</div>'}
      toc+='<a href="#d'+esc(a.dieu)+'" data-d="'+esc(a.dieu)+'">'+esc(dl(a.dieu))+'. '+esc(a.tieuDe)+'</a>';
      tx+='<article id="d'+esc(a.dieu)+'"><h3>'+esc(dl(a.dieu))+'. '+esc(a.tieuDe)+'<button type="button" data-cp="'+esc(a.dieu)+'">Sao chép trích dẫn</button></h3><div class="bd">'+esc(a.noiDung)+'</div></article>'});
    tx+='<div class="rd-src">Nguồn toàn văn: Cổng Pháp luật quốc gia (phapluat.gov.vn). Văn bản trình bày theo từng Điều (quy chuẩn kỹ thuật theo từng mục); có thể chưa gồm phụ lục, biểu mẫu, bản vẽ. Khi sử dụng chính thức, vui lòng đối chiếu bản gốc trên Cổng.</div>';
    $("#rdToc").innerHTML=toc;$("#rdTx").innerHTML=tx;
    $$("#rdToc a").forEach(function(a){a.onclick=function(e){e.preventDefault();go(a.dataset.d)}});
    $("#rdF").oninput=function(){var q=fold(this.value);$$("#rdToc a").forEach(function(a){a.hidden=q&&fold(a.textContent).indexOf(q)<0})};
    $$("#rdTx [data-cp]").forEach(function(b){b.onclick=function(){var a=arts.filter(function(x){return x.dieu===b.dataset.cp})[0];
      copy(dl(a.dieu)+". "+a.tieuDe+"\n"+a.noiDung+"\n(Trích "+name(l)+" – "+l.ten+"; nguồn: Cổng Pháp luật quốc gia)")}});
    setUrl(id,dieu);if(dieu)go(dieu);else $("#rdTx").scrollTop=0;
  }).catch(function(){$("#rdTx").innerHTML='<div class="pl-empty"><b>Không tải được toàn văn</b>Vui lòng thử lại hoặc mở trên Cổng Pháp luật quốc gia.</div>'});
}
function go(dieu){var el=document.getElementById("d"+dieu);if(!el)return;$$("#rdTx article.hl").forEach(function(x){x.classList.remove("hl")});el.classList.add("hl");
  $("#rdTx").scrollTop=el.offsetTop-$("#rdTx").offsetTop-8;$$("#rdToc a").forEach(function(a){a.classList.toggle("on",a.dataset.d===dieu)});if(cur)setUrl(cur.l.id,dieu)}
function setUrl(id,dieu){try{history.replaceState(null,"","?vb="+encodeURIComponent(id)+(dieu?"&dieu="+encodeURIComponent(dieu):""))}catch(e){}}
function closeDoc(){$("#rdOv").hidden=true;document.body.style.overflow="";cur=null;try{history.replaceState(null,"",location.pathname)}catch(e){}}
$("#rdX").onclick=closeDoc;$("#rdOv").onclick=function(e){if(e.target.id==="rdOv")closeDoc()};
document.addEventListener("keydown",function(e){if(e.key==="Escape"&&!$("#rdOv").hidden)closeDoc()});
$("#rdShare").onclick=function(){copy(location.href)};
function openFromUrl(){var q=new URLSearchParams(location.search);if(q.get("vb"))openDoc(q.get("vb"),q.get("dieu"));else if(q.get("q")){$("#plQ").value=q.get("q");search()}}

/* ---------- Tìm kiếm toàn văn ---------- */
var STOP={};"la cua va cac nhung cho trong theo duoc khi thi co khong nao gi bao nhieu toi da se the nay do voi ve mot hay hoac neu phai bi tai tu den ra vao nhu ai minh ben ma con can nen".split(" ").forEach(function(w){STOP[w]=1});
function terms(q){var w=fold(q).replace(/[^a-z0-9\s]/g," ").split(/\s+/).filter(Boolean),t={};
  for(var i=0;i<w.length-1;i++)if(!(STOP[w[i]]&&STOP[w[i+1]]))t[w[i]+" "+w[i+1]]=1;
  for(i=0;i<w.length-2;i++)t[w[i]+" "+w[i+1]+" "+w[i+2]]=1;
  w.forEach(function(x){if(!STOP[x]&&(x.length>=5||/\d/.test(x)))t[x]=1});if(w.length===1)t[w[0]]=1;return Object.keys(t)}
function occ(h,t){var n=0,i=0;while((i=h.indexOf(t,i))!==-1){n++;i+=t.length;if(n>8)break}return n}
function hl(text,ts){var ws=[];ts.forEach(function(t){t.split(" ").forEach(function(w){if(w.length>=2&&!STOP[w]&&ws.indexOf(w)<0)ws.push(w)})});
  var f=fold(text),m=[],L=/[a-z0-9]/;ws.forEach(function(w){var i=0;while((i=f.indexOf(w,i))!==-1){if(!L.test(f.charAt(i-1)||" ")&&!L.test(f.charAt(i+w.length)||" "))m.push([i,i+w.length]);i+=w.length}});
  if(!m.length)return esc(text);m.sort(function(a,b){return a[0]-b[0]});var o="",p=0;m.forEach(function(x){if(x[0]<p)return;o+=esc(text.slice(p,x[0]))+"<mark>"+esc(text.slice(x[0],x[1]))+"</mark>";p=x[1]});return o+esc(text.slice(p))}
function search(){var q=$("#plQ").value.trim();var v=V();
  if(!q){render();return}
  if(window.qcTk)qcTk("search",{search_term:q});
  var area=$("#plArea").value;
  var laws=S.laws.filter(function(l){return l.soDieu>0&&status(l)==="con"&&(area==="all"||area===AM[l.nhom])});
  $$("#plTabs button").forEach(function(b){b.setAttribute("aria-selected","false")});
  v.innerHTML='<div class="pl-load"><span class="spin"></span>Đang tìm trong '+laws.length+' văn bản…</div>';
  Promise.all(laws.map(function(l){return loadText(l.id).catch(function(){return[]})})).then(function(all){
    var ts=terms(q),sn=fold(q).trim(),hits=[];
    all.forEach(function(arts){arts.forEach(function(a){var s=0;ts.forEach(function(t){var n=occ(a._f,t);if(n){var k=t.split(" ").length;s+=Math.min(n,5)*k+(a._t.indexOf(t)>=0?6*k:0)}});if(a._f.indexOf(sn)>=0)s+=20;if(s>0)hits.push({a:a,s:s})})});
    hits.sort(function(x,y){return y.s-x.s});hits=hits.slice(0,20);
    try{history.replaceState(null,"","?q="+encodeURIComponent(q))}catch(e){}
    var back='<button type="button" class="pl-crumb" id="plBack" style="background:none;border:0;padding:0;color:var(--blue);font:inherit;font-weight:600;cursor:pointer">← Quay lại</button>';
    if(!hits.length){v.innerHTML=back+'<div class="pl-empty"><b>Không tìm thấy kết quả</b>Thử dùng thuật ngữ trong văn bản, ví dụ “giấy phép xây dựng”, “tạm ứng hợp đồng”.</div>'}
    else v.innerHTML=back+'<div class="pl-res"><h2>Kết quả cho “'+esc(q)+'”</h2><p class="sub">'+hits.length+' điều luật phù hợp nhất · chỉ tìm trong văn bản còn hiệu lực</p>'+hits.map(function(h){var a=h.a,l=S.byId[a.lawId];
      var full=a.tieuDe+" "+a.noiDung,f=a._f,pos=-1;ts.forEach(function(t){var i=f.indexOf(t);if(i>=0&&(pos<0||t.indexOf(" ")>0))pos=i});var st=Math.max(0,pos-80);
      return'<button type="button" class="pl-hit" data-l="'+esc(a.lawId)+'" data-d="'+esc(a.dieu)+'"><div class="v">'+esc(name(l))+'</div><div class="t">'+esc(dl(a.dieu))+'. '+hl(a.tieuDe,ts)+'</div><div class="s">'+(st?"…":"")+hl(full.slice(st,st+220),ts)+'…</div></button>'}).join("")+'</div>';
    $$(".pl-hit",v).forEach(function(b){b.onclick=function(){openDoc(b.dataset.l,b.dataset.d)}});
    $("#plBack").onclick=function(){$("#plQ").value="";try{history.replaceState(null,"",location.pathname)}catch(e){}setTab(S.tab)};
  });
}
$("#plForm").onsubmit=function(e){e.preventDefault();search()};
$$("#plEx button").forEach(function(b){b.onclick=function(){$("#plQ").value=b.textContent;search()}});
})();
