/* Người tạo: Quang Mai Phú – Thống kê truy cập website Quan Construction (Google Analytics 4)
   Mã đo lường: G-K7E1PQG7LT · Tạo ngày 18/10/2026
   - Đếm lượt xem trang, nguồn truy cập (Google Analytics tự thu thập, IP được ẩn danh)
   - Sự kiện riêng: goi_dien, gui_email, nhan_zalo, generate_lead (gửi form liên hệ);
     trang Pháp lý (js/phap-ly.js): xem_van_ban, search
   - Cập nhật 18/10/2026 (Quang Mai Phú): bỏ khung thông báo cookie theo yêu cầu */
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

});
})();
