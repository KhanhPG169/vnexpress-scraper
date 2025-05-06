import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time

# URL của trang chủ VnExpress
url = 'https://vnexpress.net/'

# Hàm thu thập dữ liệu
def fetch_data():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Lấy tất cả các bài viết (sử dụng các selector chính xác từ trang web)
    articles = soup.find_all('article')

    # Lưu trữ dữ liệu bài viết
    data = []

    for article in articles:
        title = article.find('h3').get_text() if article.find('h3') else 'No title'
        description = article.find('p').get_text() if article.find('p') else 'No description'
        image_url = article.find('img')['src'] if article.find('img') else 'No image'
        content_url = article.find('a')['href'] if article.find('a') else None

        if content_url:
            content_response = requests.get(content_url)
            content_soup = BeautifulSoup(content_response.text, 'html.parser')
            content = content_soup.find('article').get_text() if content_soup.find('article') else 'No content'
        else:
            content = 'No content'

        data.append({
            'Title': title,
            'Description': description,
            'Image URL': image_url,
            'Content': content,
        })

    # Lưu dữ liệu vào file CSV
    df = pd.DataFrame(data)
    df.to_csv('vnexpress_data.csv', index=False)

    print('Dữ liệu đã được lưu vào vnexpress_data.csv')

# Thiết lập lịch trình chạy vào lúc 6h sáng mỗi ngày
schedule.every().day.at("06:00").do(fetch_data)

# Chạy lịch trình
while True:
    schedule.run_pending()
    time.sleep(60)
