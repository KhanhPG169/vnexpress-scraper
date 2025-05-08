# VnExpress News Scraper

Thu thập dữ liệu bài viết từ trang https://vnexpress.net theo chuyên mục như Công nghệ, Kinh doanh, Giải trí, v.v.

## ✅ Chức năng
- Đoạn mã này sẽ thu thập dữ liệu từ một chuyên mục tin tức (ví dụ: Công nghệ) của VnExpress.
- Mỗi ngày, lúc 6h sáng, script sẽ tự động chạy, thu thập dữ liệu mới từ trang web và lưu vào một file CSV.
- Lỗi sẽ được ghi lại vào file log (errors.log), giúp bạn dễ dàng theo dõi sự cố.

## 🔧 Cài đặt
```bash
git clone https://github.com/KhanhPG169/vnexpress-scraper

cd vnexpress_scraper

Cài thư viện cần thiết
Chạy lệnh: pip install -r requirements.txt

Chạy file baitaplonv2.py:
Chạy lệnh: python baitaplonv2.py
✅ Chương trình sẽ chạy nền và đợi đến 6h sáng mỗi ngày để tự động lấy dữ liệu và lưu file CSV trong thư mục data/.
Nếu bạn muốn lưu dưới dạng Excel thay vì CSV:
Thay dòng: df.to_csv(filename, index=False, encoding='utf-8-sig')
Bằng: df.to_excel(f'data/vnexpress_articles_{today}.xlsx', index=False, encoding='utf-8-sig')

✅ (Tuỳ chọn) Kiểm tra nhanh chương trình hoạt động
Bạn có thể tạm thời sửa dòng này để test ngay (thay vì đợi 6h sáng):
schedule.every().day.at("06:00").do(job)
➡ Sửa thành:
schedule.every(1).minutes.do(job)  # Test mỗi phút
Sau khi test xong, nhớ đổi lại về 06:00.
