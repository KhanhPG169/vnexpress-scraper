# VnExpress News Scraper

Thu thập dữ liệu bài viết từ trang https://vnexpress.net theo chuyên mục như Công nghệ, Kinh doanh, Giải trí, v.v.

## ✅ Chức năng
- Tự động quét bài viết mới
- Lưu vào file CSV
- Thiết lập chạy mỗi ngày lúc 6h sáng

## 🔧 Cài đặt
```bash
git clone https://github.com/KhanhPG169/vnexpress-scraper

cd vnexpress_scraper

Cài thư viện cần thiết
Chạy lệnh: pip install -r requirements.txt

Chạy file baitaplonv2.py:
Chạy lệnh: python baitaplonv2.py
✅ Chương trình sẽ chạy nền và đợi đến 6h sáng mỗi ngày để tự động lấy dữ liệu và lưu file CSV trong thư mục data/.

✅ (Tuỳ chọn) Kiểm tra nhanh chương trình hoạt động
Bạn có thể tạm thời sửa dòng này để test ngay (thay vì đợi 6h sáng):
schedule.every().day.at("06:00").do(job)
➡ Sửa thành:
schedule.every(1).minutes.do(job)  # Test mỗi phút
Sau khi test xong, nhớ đổi lại về 06:00.
