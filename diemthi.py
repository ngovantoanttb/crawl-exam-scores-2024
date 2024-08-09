import requests
import numpy as np
from bs4 import BeautifulSoup, Tag

# Mở file CSV để ghi dữ liệu
with open('data.csv', 'w', encoding='utf-8') as w:
    # Ghi tiêu đề các cột vào file CSV
    w.write('SBD,Toán,Văn,Ngoại ngữ,Vật lý,Hóa học,Sinh học,Lịch sử,Địa lý,GDCD\n')
    
    # Duyệt qua các mã số từ 01000000 đến 64100000
    for idx in range(1000000, 64100000):

        # Định dạng idx thành chuỗi có độ dài 8 ký tự, thêm số 0 ở đầu nếu cần
        formatted_idx = str(idx).zfill(8)
        
        # Gửi yêu cầu HTTP GET tới URL tương ứng
        page = requests.get("https://vietnamnet.vn/giao-duc/diem-thi/tra-cuu-diem-thi-tot-nghiep-thpt/2024/{}.html".format(formatted_idx))
        
        # Kiểm tra mã trạng thái của phản hồi, nếu không phải 404 thì xử lý
        if page.status_code != 404:
            print("[GET] {}/64100000".format(formatted_idx))
            
            # Phân tích cú pháp HTML của trang
            soup = BeautifulSoup(page.text, "html.parser")
            elements = soup.find_all("td")
            
            # Chia các phần tử <td> thành từng cặp (n=2)
            n = 2
            elements = [elements[i:i+n] for i in range(0, len(elements), n)]
            
            # Tạo từ điển để lưu điểm số của các môn học
            subjects = {
                'Toán': '',
                'Văn': '',
                'Ngoại ngữ': '',
                'Lí': '',
                'Hóa': '',  
                'Sinh': '',
                'Sử': '',
                'Địa': '',
                'GDCD': ''
            }
            
            # Gán điểm số cho từng môn học trong từ điển
            for element in elements:
                key = element[0].text.strip()
                value = element[1].text.strip()
                if key in subjects:
                    subjects[key] = value
            
            # Tạo một dòng chứa số báo danh và điểm số của các môn học
            line = formatted_idx + ',' + ','.join([v for v in subjects.values()])

            # Ghi dòng đó vào file CSV
            w.write(line + '\n')
        else:
            print("[INFO] {}/64100000: no data".format(formatted_idx))
