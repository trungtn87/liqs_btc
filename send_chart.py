from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import time

# Cấu hình Chrome headless
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--window-size=1920,1080")

# Mở trình duyệt
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Mở trang biểu đồ Coinglass
driver.get("https://www.coinglass.com/vi/pro/futures/LiquidationHeatMap")

# Đợi trang load đầy đủ (tùy tốc độ mạng, có thể tăng lên 10-15s)
time.sleep(10)

# Tìm phần biểu đồ bằng class
try:
    chart_element = driver.find_element(By.CLASS_NAME, "heat-chart-container")  # <- class của biểu đồ
except:
    print("Không tìm thấy biểu đồ!")
    driver.quit()
    exit()

# Chụp toàn bộ màn hình
driver.save_screenshot("full_screenshot.png")

# Lấy vị trí và kích thước của biểu đồ
location = chart_element.location
size = chart_element.size

# Crop lại phần biểu đồ từ ảnh chụp màn hình
image = Image.open("full_screenshot.png")
left = location['x']
top = location['y']
right = location['x'] + size['width']
bottom = location['y'] + size['height']

chart_image = image.crop((left, top, right, bottom))
chart_image.save("chart.png")

print("✅ Đã lưu ảnh biểu đồ thành chart.png")

driver.quit()
