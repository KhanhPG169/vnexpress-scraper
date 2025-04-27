import os
import shutil
import smtplib
import schedule
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Tải file .env để lấy thông tin mail
load_dotenv()

# Lấy thông tin từ file .env
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
BACKUP_FOLDER = "C:/Backup"  # Đường dẫn thư mục backup

def backup_database():
    try:
        # Duyệt qua các file trong thư mục hiện tại
        for filename in os.listdir('.'):
            if filename.endswith('.sql') or filename.endswith('.sqlite3'):
                # Đường dẫn đầy đủ của file database
                src_path = os.path.join(os.getcwd(), filename)
                # Đường dẫn backup
                dest_path = os.path.join(BACKUP_FOLDER, filename)
                # Copy file đến thư mục backup
                shutil.copy(src_path, dest_path)
                print(f"Đã sao lưu: {filename}")
        
        # Gửi email thông báo thành công
        send_email("Backup thành công", "Backup file cơ sở dữ liệu đã được thực hiện thành công.")
        
    except Exception as e:
        # Nếu có lỗi xảy ra, gửi email thông báo lỗi
        send_email("Backup thất bại", f"Đã xảy ra lỗi khi backup: {str(e)}")

def send_email(subject, body):
    try:
        # Tạo đối tượng message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Kết nối SMTP và gửi email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            text = msg.as_string()
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
            print(f"Đã gửi email thông báo: {subject}")
    
    except Exception as e:
        print(f"Không thể gửi email: {str(e)}")

# Lên lịch chạy hàm backup_database mỗi ngày lúc 00:00 AM
schedule.every().day.at("00:00").do(backup_database)

# Chạy công việc đã lên lịch
while True:
    schedule.run_pending()
    time.sleep(60)  # Kiểm tra mỗi phút
