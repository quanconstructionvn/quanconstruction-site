/* Người tạo: Quang Mai Phú – Tra cứu pháp luật xây dựng, nhà ở & đất đai (Quan Construction)
   Cập nhật 18/10/2026 (Quang Mai Phú): thêm nhóm D–H (đất đai, nhà ở, quy hoạch, thuế phí, xử phạt), lọc lĩnh vực, Hành trình pháp lý một ngôi nhà
   Dữ liệu: phap-ly/danh-muc.json + phap-ly/van-ban/<id>.json (mỗi điều: [số điều, tiêu đề, nội dung, chương])
   Nguồn toàn văn: Cổng Pháp luật quốc gia (phapluat.gov.vn) */
(function(){
"use strict";
var $=function(s,r){return(r||document).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
var esc=function(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]})};
var fold=function(s){return String(s||"").normalize("NFD").replace(/[̀-ͯ]/g,"").replace(/đ/g,"d").replace(/Đ/g,"D").toLowerCase()};
var p2=function(n){return(n<10?"0":"")+n};
var d=new Date(),TODAY=d.getFullYear()+"-"+p2(d.getMonth()+1)+"-"+p2(d.getDate());
var fmt=function(x){return x?x.split("-").reverse().join("/"):"—"};
var GROUPS=[["A","A","Nền tảng pháp lý – Văn bản Luật"],["B1","B.I","Quản lý hoạt động xây dựng"],["B2","B.II","Quản lý chi phí đầu tư xây dựng"],["B3","B.III","Quản lý hợp đồng xây dựng"],["B4","B.IV","Quản lý chất lượng, thi công và bảo trì"],["B5","B.V","Quản lý vật liệu xây dựng"],["B6","B.VI","Năng lực, hệ thống thông tin & CSDL"],["B7","B.VII","Thanh toán – Quyết toán vốn đầu tư dự án"],["C","C","Pháp luật dân sự, thương mại, đấu thầu"],["D","D","Đất đai & Giấy chứng nhận (sổ đỏ)"],["E","E","Nhà ở & kinh doanh bất động sản"],["F","F","Quy hoạch đô thị và nông thôn"],["G","G","Công chứng, thuế & lệ phí nhà đất"],["H","H","Xử phạt vi phạm hành chính"]];
var NHA={D:1,E:1,F:1,G:1,H:1};
var GM={};GROUPS.forEach(function(g){GM[g[0]]=g});
var S={laws:[],byId:{},texts:{},group:"all",showOld:false};
function status(l){if(l.hieuLucTu&&TODAY<l.hieuLucTu)return"chua";if(l.hieuLucDen&&TODAY>=l.hieuLucDen)return"het";return"con"}
var STL={con:"Còn hiệu lực",het:"Hết hiệu lực",chua:"Chưa có hiệu lực"};
function name(l){return(l.loai||"")+" "+(l.soHieu||"")}
function toast(m){var t=$("#plToast");t.textContent=m;t.hidden=false;clearTimeout(toast.t);toast.t=setTimeout(function(){t.hidden=true},2400)}
function copy(t){var ok=function(){toast("Đã sao chép")};if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(ok,function(){fb()})}else fb();
  function fb(){var a=document.createElement("textarea");a.value=t;document.body.appendChild(a);a.select();try{document.execCommand("copy");ok()}catch(e){toast("Hãy bôi đen để sao chép")}a.remove()}}

/* ---------- Danh mục ---------- */
fetch("phap-ly/danh-muc.json").then(function(r){return r.json()}).then(function(j){
  S.laws=j.vanBan;S.laws.forEach(function(l){S.byId[l.id]=l});
  $("#plUpd").textContent=fmt(j.capNhat);
  renderChips();renderList();openFromUrl();
}).catch(function(){$("#plList").innerHTML='<div class="pl-empty"><b>Không tải được danh mục</b>Vui lòng tải lại trang.</div>'});

function renderChips(){
  var used=GROUPS.filter(function(g){return S.laws.some(function(l){return l.nhom===g[0]})});
  $("#plChips").innerHTML='<button type="button" data-g="all" aria-pressed="'+(S.group==="all")+'">Tất cả</button>'+used.map(function(g){return'<button type="button" data-g="'+g[0]+'" aria-pressed="'+(S.group===g[0])+'"><b>'+g[1]+'</b>'+esc(g[2])+'</button>'}).join("");
  $$("#plChips button").forEach(function(b){b.onclick=function(){S.group=b.dataset.g;renderChips();renderList()}});
}
function renderList(){
  var vis=S.laws.filter(function(l){return(S.showOld||status(l)!=="het")&&(S.group==="all"||l.nhom===S.group)});
  $("#plCount").textContent=vis.length+" văn bản · "+vis.filter(function(l){return l.soDieu>0}).length+" có toàn văn";
  var h="";GROUPS.forEach(function(g){
    var xs=vis.filter(function(l){return l.nhom===g[0]}).sort(function(a,b){return(a.thuTu||99)-(b.thuTu||99)});if(!xs.length)return;
    h+='<div class="pl-grp" id="nhom-'+g[0]+'"><h2><span>'+g[1]+'</span>'+esc(g[2])+'<small>'+xs.length+' văn bản</small></h2><div class="pl-list">'+xs.map(row).join("")+'</div></div>';
  });
  $("#plList").innerHTML=h||'<div class="pl-empty"><b>Không có văn bản phù hợp</b>Chọn nhóm khác hoặc bật "Hiện văn bản đã hết hiệu lực".</div>';
  $$("#plList [data-read]").forEach(function(b){b.onclick=function(){openDoc(b.dataset.read)}});
}
function row(l){var st=status(l);var mp=l.ttCong&&/một phần/.test(l.ttCong)&&st==="con";
  return'<div class="pl-row"><div style="min-width:0"><div class="sh2">'+esc(name(l))+(l.nhanh?'<em>'+esc(l.nhanh)+'</em>':"")+'</div><p>'+esc(l.ten)+'</p>'+
  '<div class="mt"><span>Ban hành: '+fmt(l.ngayBanHanh)+'</span><span>Hiệu lực: '+fmt(l.hieuLucTu)+(l.hieuLucDen?" → "+fmt(l.hieuLucDen):"")+'</span><span class="st '+st+'">'+STL[st]+'</span>'+(mp?'<span class="st mp">Hết hiệu lực một phần</span>':"")+(l.biThayThe?'<span>Thay thế bởi: '+esc(l.biThayThe)+'</span>':"")+'</div></div>'+
  '<div class="act">'+(l.soDieu>0?'<button type="button" class="rd" data-read="'+esc(l.id)+'">Đọc toàn văn · '+l.soDieu+' điều</button>':"")+(l.linkCong?'<a class="ex" href="'+esc(l.linkCong)+'" target="_blank" rel="noopener">Cổng Pháp luật ↗</a>':"")+'</div></div>'}
$("#plOld").onchange=function(){S.showOld=this.checked;renderList()};

/* ---------- Toàn văn ---------- */
function loadText(id){if(S.texts[id])return Promise.resolve(S.texts[id]);
  return fetch("phap-ly/van-ban/"+encodeURIComponent(id)+".json").then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(a){
    var arts=a.map(function(x){return{dieu:x[0],tieuDe:x[1],noiDung:x[2],chuong:x[3],lawId:id,_f:fold(x[1]+" "+x[2]),_t:fold(x[1])}});S.texts[id]=arts;return arts})}
var cur=null;
function openDoc(id,dieu){var l=S.byId[id];if(!l)return;
  $("#rdT").textContent=name(l);$("#rdS").textContent=l.ten+" · Hiệu lực "+fmt(l.hieuLucTu)+(l.hieuLucDen?" → "+fmt(l.hieuLucDen):"");
  var lk=$("#rdLink");if(l.linkCong){lk.href=l.linkCong;lk.hidden=false}else lk.hidden=true;
  $("#rdTx").innerHTML='<div class="pl-load"><span class="spin"></span>Đang tải toàn văn…</div>';$("#rdToc").innerHTML="";
  $("#rdOv").hidden=false;document.body.style.overflow="hidden";
  loadText(id).then(function(arts){cur={l:l,arts:arts};
    var ch="",toc='<input type="search" id="rdF" placeholder="Lọc theo tên điều…" aria-label="Lọc điều">',tx="";
    arts.forEach(function(a){if(a.chuong&&a.chuong!==ch){ch=a.chuong;toc+='<div class="ch">'+esc(ch.split(" – ")[0])+'</div>';tx+='<div class="chp">'+esc(ch)+'</div>'}
      toc+='<a href="#d'+esc(a.dieu)+'" data-d="'+esc(a.dieu)+'">Điều '+esc(a.dieu)+'. '+esc(a.tieuDe)+'</a>';
      tx+='<article id="d'+esc(a.dieu)+'"><h3>Điều '+esc(a.dieu)+'. '+esc(a.tieuDe)+'<button type="button" data-cp="'+esc(a.dieu)+'">Sao chép trích dẫn</button></h3><div class="bd">'+esc(a.noiDung)+'</div></article>'});
    tx+='<div class="rd-src">Nguồn toàn văn: Cổng Pháp luật quốc gia (phapluat.gov.vn). Văn bản trình bày theo từng Điều, chưa gồm phụ lục, biểu mẫu. Khi sử dụng chính thức, vui lòng đối chiếu bản gốc trên Cổng.</div>';
    $("#rdToc").innerHTML=toc;$("#rdTx").innerHTML=tx;
    $$("#rdToc a").forEach(function(a){a.onclick=function(e){e.preventDefault();go(a.dataset.d)}});
    $("#rdF").oninput=function(){var q=fold(this.value);$$("#rdToc a").forEach(function(a){a.hidden=q&&fold(a.textContent).indexOf(q)<0})};
    $$("#rdTx [data-cp]").forEach(function(b){b.onclick=function(){var a=arts.filter(function(x){return x.dieu===b.dataset.cp})[0];
      copy("Điều "+a.dieu+". "+a.tieuDe+"\n"+a.noiDung+"\n(Trích "+name(l)+" – "+l.ten+"; nguồn: Cổng Pháp luật quốc gia)")}});
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
function search(){var q=$("#plQ").value.trim();var box=$("#plRes");
  if(!q){box.innerHTML="";box.hidden=true;$("#plCat").hidden=false;return}
  box.hidden=false;$("#plCat").hidden=true;
  var scope=$("#plScope").value;
  var area=$("#plArea").value;
  var laws=S.laws.filter(function(l){return l.soDieu>0&&(scope==="all"||status(l)==="con")&&(area==="all"||(area==="nha")===!!NHA[l.nhom])});
  box.innerHTML='<div class="pl-load"><span class="spin"></span>Đang tìm trong '+laws.length+' văn bản…</div>';
  Promise.all(laws.map(function(l){return loadText(l.id).catch(function(){return[]})})).then(function(all){
    var ts=terms(q),sn=fold(q).trim(),hits=[];
    all.forEach(function(arts){arts.forEach(function(a){var s=0;ts.forEach(function(t){var n=occ(a._f,t);if(n){var k=t.split(" ").length;s+=Math.min(n,5)*k+(a._t.indexOf(t)>=0?6*k:0)}});if(a._f.indexOf(sn)>=0)s+=20;if(s>0)hits.push({a:a,s:s})})});
    hits.sort(function(x,y){return y.s-x.s});hits=hits.slice(0,30);
    try{history.replaceState(null,"","?q="+encodeURIComponent(q))}catch(e){}
    if(!hits.length){box.innerHTML='<div class="pl-empty"><b>Không tìm thấy kết quả</b>Thử dùng thuật ngữ trong văn bản, ví dụ "tạm ứng hợp đồng", "bảo lãnh thực hiện hợp đồng".</div>';return}
    box.innerHTML='<h2>'+hits.length+' điều luật phù hợp nhất với “'+esc(q)+'”</h2><button type="button" class="btn g" id="plBack" style="padding:8px 16px;margin-bottom:14px">← Về danh mục văn bản</button>'+hits.map(function(h){var a=h.a,l=S.byId[a.lawId];
      var full=a.tieuDe+" "+a.noiDung,f=a._f,pos=-1;ts.forEach(function(t){var i=f.indexOf(t);if(i>=0&&(pos<0||t.indexOf(" ")>0))pos=i});var st=Math.max(0,pos-90);
      return'<button type="button" class="pl-hit" data-l="'+esc(a.lawId)+'" data-d="'+esc(a.dieu)+'"><div class="v">'+esc(name(l))+' · '+STL[status(l)]+'</div><div class="t">Điều '+esc(a.dieu)+'. '+hl(a.tieuDe,ts)+'</div><div class="s">'+(st?"…":"")+hl(full.slice(st,st+280),ts)+'…</div></button>'}).join("");
    $$("#plRes .pl-hit").forEach(function(b){b.onclick=function(){openDoc(b.dataset.l,b.dataset.d)}});
    $("#plBack").onclick=function(){$("#plQ").value="";search()};
  });
}
$$("#hanh-trinh a[data-vb]").forEach(function(a){a.onclick=function(e){if(!S.byId[a.dataset.vb])return;e.preventDefault();openDoc(a.dataset.vb,a.dataset.dieu)}});
$("#plForm").onsubmit=function(e){e.preventDefault();search()};
$$("#plEx button").forEach(function(b){b.onclick=function(){$("#plQ").value=b.textContent;search()}});
})();
