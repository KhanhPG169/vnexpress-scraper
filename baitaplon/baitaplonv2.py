import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import schedule
import time
import os

# Tạo thư mục lưu nếu chưa tồn tại
os.makedirs("data", exist_ok=True)

# Header giả lập trình duyệt
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36'
}

def scrape_articles(category_url):
    articles = []

    try:
        res = requests.get(category_url, headers=headers)
        res.raise_for_status()
    except Exception as e:
        print("Lỗi khi truy cập trang chuyên mục:", e)
        return []

    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.select('article.item-news')

    for item in items:
        try:
            title_tag = item.select_one('h3.title-news a')
            title = title_tag.text.strip()
            link = title_tag['href']
            desc = item.select_one('p.description').text.strip() if item.select_one('p.description') else ''
            img = item.select_one('img')['src'] if item.select_one('img') else ''

            # Truy cập vào bài viết chi tiết
            detail_res = requests.get(link, headers=headers)
            detail_res.raise_for_status()

            detail_soup = BeautifulSoup(detail_res.text, 'html.parser')
            paragraphs = detail_soup.select('article.fck_detail p')
            content = ' '.join(p.text.strip() for p in paragraphs) if paragraphs else 'Không có nội dung chi tiết.'

            articles.append({
                'Tiêu đề': title,
                'Mô tả': desc,
                'Hình ảnh': img,
                'Nội dung': content,
                'Link': link
            })

            time.sleep(1)  # Nghỉ 1 giây giữa các lần request để tránh bị chặn

        except Exception as e:
            print("Lỗi xử lý bài viết:", e)
            with open("data/errors.log", "a", encoding="utf-8") as f:
                f.write(f"{datetime.now()} - Lỗi: {e} - Link: {link if 'link' in locals() else 'Không xác định'}\n")

    return articles

def save_to_csv(data):
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f'data/vnexpress_articles_{today}.csv'
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"Đã lưu file: {filename}")

def job():
    print(f"\nBắt đầu lấy dữ liệu lúc {datetime.now().strftime('%H:%M:%S')}")
    category_url = 'https://vnexpress.net/cong-nghe'  # Có thể đổi chuyên mục khác
    articles = scrape_articles(category_url)
    if articles:
        save_to_csv(articles)
    else:
        print("Không có bài viết nào được thu thập.")
    print(f"Hoàn tất lúc {datetime.now().strftime('%H:%M:%S')}\n")

# Thiết lập chạy mỗi ngày lúc 6h sáng
schedule.every().day.at("06:00").do(job)

if __name__ == '__main__':
    print("Trình thu thập dữ liệu đang chạy... Đợi đến 6h sáng mỗi ngày.")
    while True:
        schedule.run_pending()
        time.sleep(60)
