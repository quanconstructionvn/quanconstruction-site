/* Người tạo: Quang Mai Phú – đọc nội dung từ /content/*.json do trang /admin cập nhật */
(function(){
var F={news:'content/tin-tuc.json',projects:'content/cong-trinh.json',jobs:'content/tuyen-dung.json'};
function e(t,c,x){var n=document.createElement(t);if(c)n.className=c;if(x!=null)n.textContent=x;return n}
function img(src,alt){if(!src)return null;var i=e('img');i.src=src.replace(/^\//,'');i.alt=alt||'';i.loading='lazy';return i}
var R={
news:function(o){var c=e('div','news rv in');c.appendChild(e('small','',o.date||''));c.appendChild(e('h3','',o.title));c.appendChild(e('p','',o.summary||''));
 var m=img(o.image,o.title);if(m){m.className='nimg';c.insertBefore(m,c.firstChild)}return c},
projects:function(o){var c=e('div','prj rv in');var m=img(o.image,o.title);if(m)c.appendChild(m);var b=e('div','pb');b.appendChild(e('small','',[o.category,o.year].filter(Boolean).join(' · ')));b.appendChild(e('h3','',o.title));if(o.location)b.appendChild(e('em','',o.location));b.appendChild(e('p','',o.summary||''));c.appendChild(b);return c},
jobs:function(o){var c=e('div','job rv in');c.appendChild(e('h3','',o.title));c.appendChild(e('small','',[o.quantity&&('Số lượng: '+o.quantity),o.place,o.deadline&&('Hạn nộp: '+o.deadline)].filter(Boolean).join(' · ')));c.appendChild(e('p','',o.desc||''));
 var a=e('a','btn p','Ứng tuyển');a.href='mailto:quanconstruction.vn@gmail.com?subject='+encodeURIComponent('Ứng tuyển: '+o.title);c.appendChild(a);return c}};
document.querySelectorAll('[data-feed]').forEach(function(box){
 var k=box.getAttribute('data-feed'),lim=parseInt(box.getAttribute('data-limit')||'0',10),cat=box.getAttribute('data-cat');
 fetch(F[k]+'?v='+Date.now()).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(d){
  var it=(d.items||[]).filter(function(o){return !cat||o.category===cat});
  if(k==='news')it=it.slice().reverse();
  if(lim)it=it.slice(0,lim);
  if(!it.length)return;box.innerHTML='';it.forEach(function(o){box.appendChild(R[k](o))})
 }).catch(function(){})});
})();
