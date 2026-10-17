/* Người tạo: Quang Mai Phú – đọc nội dung từ /content/*.json do trang /admin cập nhật */
(function(){
var EN=document.documentElement.lang==='en',P=EN?'../':'';
var F={news:P+'content/tin-tuc.json',projects:P+'content/cong-trinh.json',jobs:P+'content/tuyen-dung.json'};
var CAT={'Dân dụng':'Residential','Công nghiệp':'Industrial','Nhôm kính':'Aluminium & glass'};
var T=EN?{qty:'Quantity: ',dl:'Deadline: ',ap:'Apply',sub:'Application: '}:{qty:'Số lượng: ',dl:'Hạn nộp: ',ap:'Ứng tuyển',sub:'Ứng tuyển: '};
function L(o,k){if(!EN)return o[k];return o[k+'_en']}
function ok(o,k){return !EN||!!(o[k+'_en']&&String(o[k+'_en']).trim())}
function e(t,c,x){var n=document.createElement(t);if(c)n.className=c;if(x!=null)n.textContent=x;return n}
function img(src,alt){if(!src)return null;var i=e('img');i.src=P+src.replace(/^\//,'');i.alt=alt||'';i.loading='lazy';return i}
var R={
news:function(o){var c=e('div','news rv in');c.appendChild(e('small','',o.date||''));c.appendChild(e('h3','',L(o,'title')));c.appendChild(e('p','',L(o,'summary')||''));
 var m=img(o.image,L(o,'title'));if(m){m.className='nimg';c.insertBefore(m,c.firstChild)}return c},
projects:function(o){var c=e('div','prj rv in');var m=img(o.image,L(o,'title'));if(m)c.appendChild(m);var b=e('div','pb');b.appendChild(e('small','',[EN?(CAT[o.category]||o.category):o.category,o.year].filter(Boolean).join(' · ')));b.appendChild(e('h3','',L(o,'title')));var lc=EN?(o.location_en||o.location):o.location;if(lc)b.appendChild(e('em','',lc));b.appendChild(e('p','',L(o,'summary')||''));c.appendChild(b);return c},
jobs:function(o){var c=e('div','job rv in');c.appendChild(e('h3','',L(o,'title')));c.appendChild(e('small','',[o.quantity&&(T.qty+o.quantity),EN?(o.place_en||o.place):o.place,o.deadline&&(T.dl+o.deadline)].filter(Boolean).join(' · ')));c.appendChild(e('p','',L(o,'desc')||''));
 var a=e('a','btn p',T.ap);a.href='mailto:quanconstruction.vn@gmail.com?subject='+encodeURIComponent(T.sub+L(o,'title'));c.appendChild(a);return c}};
document.querySelectorAll('[data-feed]').forEach(function(box){
 var k=box.getAttribute('data-feed'),lim=parseInt(box.getAttribute('data-limit')||'0',10),cat=box.getAttribute('data-cat');
 fetch(F[k]+'?v='+Date.now()).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(d){
  var it=(d.items||[]).filter(function(o){return (!cat||o.category===cat)&&ok(o,'title')});
  if(k==='news')it=it.slice().reverse();
  if(lim)it=it.slice(0,lim);
  if(!it.length)return;box.innerHTML='';it.forEach(function(o){box.appendChild(R[k](o))})
 }).catch(function(){})});
})();
