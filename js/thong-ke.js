/* Người tạo: Quang Mai Phú – Thống kê truy cập website Quan Construction (Google Analytics 4)
   Mã đo lường: G-K7E1PQG7LT · Tạo ngày 18/10/2026
   - Đếm lượt xem trang, nguồn truy cập (Google Analytics tự thu thập, IP được ẩn danh)
   - Sự kiện riêng: goi_dien, gui_email, nhan_zalo, generate_lead (gửi form liên hệ);
     trang Pháp lý (js/phap-ly.js): xem_van_ban, search
   - Thông báo cookie: khách có thể Từ chối → ngừng lưu cookie thống kê trên máy khách */
(function(){
"use strict";
var ID="G-K7E1PQG7LT",KEY="qc_thongke";
var get=function(){try{return localStorage.getItem(KEY)}catch(e){return null}};
var set=function(v){try{localStorage.setItem(KEY,v)}catch(e){}};
window.dataLayer=window.dataLayer||[];
function gtag(){dataLayer.push(arguments)}
window.gtag=gtag;
var tuChoi=get()==="tu-choi";
gtag("consent","default",{analytics_storage:tuChoi?"denied":"granted",ad_storage:"denied",ad_user_data:"denied",ad_personalization:"denied"});
gtag("js",new Date());
gtag("config",ID);
var s=document.createElement("script");s.async=true;s.src="https://www.googletagmanager.com/gtag/js?id="+ID;
document.head.appendChild(s);

/* Hàm dùng chung cho các trang: window.qcTk("ten_su_kien",{...}) */
window.qcTk=function(ten,thamSo){try{gtag("event",ten,thamSo||{})}catch(e){}};

function ready(fn){if(document.readyState!=="loading")fn();else document.addEventListener("DOMContentLoaded",fn)}
ready(function(){
  /* Bấm gọi điện / email / Zalo */
  document.addEventListener("click",function(e){
    var a=e.target.closest&&e.target.closest("a[href]");if(!a)return;
    var h=a.getAttribute("href")||"";
    if(/^tel:/i.test(h))qcTk("goi_dien",{vi_tri:location.pathname});
    else if(/^mailto:/i.test(h))qcTk("gui_email",{vi_tri:location.pathname});
    else if(/zalo\.me/i.test(h))qcTk("nhan_zalo",{vi_tri:location.pathname});
  },true);
  /* Gửi form liên hệ */
  var f=document.getElementById("cf");
  if(f)f.addEventListener("submit",function(){var l=f.elements.loai;qcTk("generate_lead",{nhu_cau:l?l.value:""})},true);

  /* Thông báo cookie (chỉ hiện lần đầu) */
  if(get())return;
  var EN=document.documentElement.lang==="en";
  var t=EN?{m:"This website uses Google Analytics cookies to count visits anonymously and improve our content.",ok:"Accept",no:"Decline"}
          :{m:"Website sử dụng cookie Google Analytics để thống kê lượt truy cập ẩn danh, giúp chúng tôi cải thiện nội dung.",ok:"Đồng ý",no:"Từ chối"};
  var b=document.createElement("div");
  b.setAttribute("role","region");b.setAttribute("aria-label",EN?"Cookie notice":"Thông báo cookie");
  b.style.cssText="position:fixed;left:16px;right:16px;bottom:16px;z-index:200;max-width:420px;background:#0a1d3f;color:#fff;border-radius:14px;padding:14px 16px;box-shadow:0 14px 40px rgba(0,0,0,.3);font-size:13.5px;line-height:1.5;display:flex;gap:12px;flex-wrap:wrap;align-items:center";
  b.innerHTML='<span style="flex:1 1 220px">'+t.m+'</span><span style="display:flex;gap:8px"><button type="button" data-v="tu-choi" style="font:inherit;font-weight:600;background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.5);border-radius:8px;padding:7px 12px;cursor:pointer">'+t.no+'</button><button type="button" data-v="dong-y" style="font:inherit;font-weight:700;background:#f5a524;color:#0a1d3f;border:0;border-radius:8px;padding:7px 14px;cursor:pointer">'+t.ok+'</button></span>';
  b.addEventListener("click",function(e){var v=e.target.getAttribute&&e.target.getAttribute("data-v");if(!v)return;
    set(v);if(v==="tu-choi")gtag("consent","update",{analytics_storage:"denied"});b.remove()});
  document.body.appendChild(b);
});
})();
