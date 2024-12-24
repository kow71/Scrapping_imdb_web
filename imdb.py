import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# Khởi tạo trình duyệt Selenium
service = Service(executable_path='D:/chromedriver-win32/chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Truy cập trang IMDb top chart
driver.get("https://www.imdb.com/chart/top")

# Lấy nội dung trang và chuyển đổi thành BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'lxml')

# Tìm phần chứa các bộ phim
movies_tag = soup.find('ul', {"class": "ipc-metadata-list"})
movies = movies_tag.find_all('li')

# Danh sách để lưu thông tin các bộ phim
list_movies = []

# Lặp qua các bộ phim và trích xuất dữ liệu
for movie in movies:
    image_url = movie.find('img').attrs['src']
    title = movie.find('h3').text

    # Lấy metadata (năm, thời gian, và đánh giá nếu có)
    metadata_items = movie.find_all('span', {"class": "cli-title-metadata-item"})

    if len(metadata_items) == 3:
        year, duration, rate = metadata_items
    else:
        year, duration = metadata_items
        rate = None

    # Lấy đánh giá và số lượng đánh giá
    rating = movie.find('span', {"class": "ipc-rating-star"})
    rating, rating_count = rating.text.split()
    rating_count = rating_count.replace("(", "").replace(")", "")

    # Thêm thông tin vào danh sách
    list_movies.append({
        "image_url": image_url,
        "title": title,
        "year": year.text,
        "duration": duration.text,
        "rate": rate.text if rate is not None else None,
        "rating": rating,
        "rating_count": rating_count,
    })

# Chuyển danh sách vào DataFrame của pandas
df = pd.DataFrame(list_movies)

# Lưu vào file CSV
df.to_csv('top_movies.csv', index=False)

# In thông báo khi hoàn tất
print("Dữ liệu đã được lưu vào 'top_movies.csv'.")

# Đóng trình duyệt
driver.quit()
