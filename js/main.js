(function(){var h=document.querySelector('header');function f(){h.classList.toggle('s',scrollY>30)}f();addEventListener('scroll',f,{passive:true});
var b=document.querySelector('.burger'),n=document.querySelector('nav');if(b)b.onclick=function(){n.classList.toggle('o')};
var io=new IntersectionObserver(function(e){e.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{threshold:.12});
document.querySelectorAll('.rv').forEach(function(e){io.observe(e)});
var fm=document.getElementById('cf');if(fm)fm.onsubmit=function(e){e.preventDefault();var g=function(i){return fm.elements[i].value.trim()};
var body='Họ tên: '+g('ten')+'\nĐiện thoại: '+g('sdt')+'\nNhu cầu: '+g('loai')+'\n\n'+g('nd');
var btn=fm.querySelector('button'),nt=fm.querySelector('.note'),t0=btn.textContent;btn.disabled=true;btn.textContent='Đang gửi…';
var fb=function(){location.href='mailto:quanconstruction.vn@gmail.com?subject='+encodeURIComponent('Liên hệ từ website - '+g('ten'))+'&body='+encodeURIComponent(body)};
fetch('https://formsubmit.co/ajax/quanconstruction.vn@gmail.com',{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify({_subject:'Liên hệ từ website - '+g('ten'),'Họ tên':g('ten'),'Điện thoại':g('sdt'),'Nhu cầu':g('loai'),'Nội dung':g('nd'),_template:'table',_captcha:'false'})})
.then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(){fm.reset();btn.disabled=false;btn.textContent=t0;nt.textContent='Đã gửi yêu cầu. Quan Construction sẽ liên hệ lại với bạn sớm nhất.'})
.catch(function(){btn.disabled=false;btn.textContent=t0;fb()})}})();