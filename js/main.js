(function(){var h=document.querySelector('header');function f(){h.classList.toggle('s',scrollY>30)}f();addEventListener('scroll',f,{passive:true});
var b=document.querySelector('.burger'),n=document.querySelector('nav');if(b)b.onclick=function(){n.classList.toggle('o')};
var io=new IntersectionObserver(function(e){e.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{threshold:.12});
document.querySelectorAll('.rv').forEach(function(e){io.observe(e)});
var EN=document.documentElement.lang==='en';var X=EN?{n:'Name: ',p:'Phone: ',d:'Need: ',s:'Website contact - ',w:'Sending…',ok:'Request sent. Quan Construction will get back to you as soon as possible.',jn:'Họ tên',jp:'Điện thoại',jd:'Nhu cầu',jc:'Nội dung'}:{n:'Họ tên: ',p:'Điện thoại: ',d:'Nhu cầu: ',s:'Liên hệ từ website - ',w:'Đang gửi…',ok:'Đã gửi yêu cầu. Quan Construction sẽ liên hệ lại với bạn sớm nhất.',jn:'Họ tên',jp:'Điện thoại',jd:'Nhu cầu',jc:'Nội dung'};var fm=document.getElementById('cf');if(fm)fm.onsubmit=function(e){e.preventDefault();var g=function(i){return fm.elements[i].value.trim()};
var body=X.n+g('ten')+'\n'+X.p+g('sdt')+'\n'+X.d+g('loai')+'\n\n'+g('nd');
var btn=fm.querySelector('button'),nt=fm.querySelector('.note'),t0=btn.textContent;btn.disabled=true;btn.textContent=X.w;
var fb=function(){location.href='mailto:quanconstruction.vn@gmail.com?subject='+encodeURIComponent(X.s+g('ten'))+'&body='+encodeURIComponent(body)};
fetch('https://formsubmit.co/ajax/quanconstruction.vn@gmail.com',{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify({_subject:X.s+g('ten'),'Họ tên':g('ten'),'Điện thoại':g('sdt'),'Nhu cầu':g('loai'),'Nội dung':g('nd'),_template:'table',_captcha:'false'})})
.then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(){fm.reset();btn.disabled=false;btn.textContent=t0;nt.textContent=X.ok})
.catch(function(){btn.disabled=false;btn.textContent=t0;fb()})}})();