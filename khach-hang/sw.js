// Người tạo: Quang Mai Phú
// Service worker tối giản: đủ điều kiện cài app; dữ liệu luôn lấy trực tiếp từ máy chủ (không lưu cache dữ liệu dự án).
self.addEventListener('install',function(){self.skipWaiting()});
self.addEventListener('activate',function(e){e.waitUntil(self.clients.claim())});
self.addEventListener('fetch',function(e){});
