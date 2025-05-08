import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import schedule
import time
import os

# Tạo thư mục lưu nếu chưa tồn tại
os.makedirs("data", exist_ok=True)

def scrape_articles(category_url):
    articles = []

    res = requests.get(category_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    items = soup.select('article.item-news')
    for item in items:
        try:
            title = item.select_one('h3.title-news a').text.strip()
            link = item.select_one('h3.title-news a')['href']
            desc = item.select_one('p.description').text.strip() if item.select_one('p.description') else ''
            img = item.select_one('img')['src'] if item.select_one('img') else ''

            # Truy cập vào bài viết chi tiết
            detail_res = requests.get(link)
            detail_soup = BeautifulSoup(detail_res.text, 'html.parser')
            content = ' '.join(p.text for p in detail_soup.select('article.fck_detail p'))

            articles.append({
                'Tiêu đề': title,
                'Mô tả': desc,
                'Hình ảnh': img,
                'Nội dung': content,
                'Link': link
            })
        except Exception as e:
            print("Lỗi xử lý bài viết:", e)

    return articles

def save_to_csv(data):
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f'data/vnexpress_articles_{today}.csv'
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"Đã lưu file: {filename}")

def job():
    print(f"Bắt đầu lấy dữ liệu lúc {datetime.now().strftime('%H:%M:%S')}")
    category_url = 'https://vnexpress.net/cong-nghe'  # Có thể đổi chuyên mục khác
    articles = scrape_articles(category_url)
    save_to_csv(articles)
    print(f"Hoàn tất lúc {datetime.now().strftime('%H:%M:%S')}\n")

# Thiết lập chạy mỗi ngày lúc 6h sáng
schedule.every().day.at("06:00").do(job)

if __name__ == '__main__':
    print("Trình thu thập dữ liệu đang chạy... Đợi đến 6h sáng mỗi ngày.")
    while True:
        schedule.run_pending()
        time.sleep(60)
