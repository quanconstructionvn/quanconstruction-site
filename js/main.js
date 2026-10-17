(function(){var h=document.querySelector('header');function f(){h.classList.toggle('s',scrollY>30)}f();addEventListener('scroll',f,{passive:true});
var b=document.querySelector('.burger'),n=document.querySelector('nav');if(b)b.onclick=function(){n.classList.toggle('o')};
var io=new IntersectionObserver(function(e){e.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{threshold:.12});
document.querySelectorAll('.rv').forEach(function(e){io.observe(e)});
var fm=document.getElementById('cf');if(fm)fm.onsubmit=function(e){e.preventDefault();var g=function(i){return fm.elements[i].value.trim()};
var body='Họ tên: '+g('ten')+'\nĐiện thoại: '+g('sdt')+'\nNhu cầu: '+g('loai')+'\n\n'+g('nd');
location.href='mailto:quanconstruction.vn@gmail.com?subject='+encodeURIComponent('Liên hệ từ website - '+g('ten'))+'&body='+encodeURIComponent(body)}})();
