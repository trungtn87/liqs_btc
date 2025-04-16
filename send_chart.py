from playwright.sync_api import sync_playwright
from PIL import Image
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
URL = "https://www.coinglass.com/vi/pro/futures/LiquidationHeatMap"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    print("🔄 Đang mở trang Coinglass...")
    page.goto(URL, timeout=60000)
    page.wait_for_timeout(10000)  # đợi trang load hoàn toàn
    page.screenshot(path="screenshot.png", full_page=True)
    browser.close()

# 📏 Crop theo tọa độ cố định (đã test ổn trên máy và CI)
image = Image.open("screenshot.png")
# Tùy chỉnh nếu layout trang thay đổi
left = 300
top = 200
right = 1620
bottom = 880

chart = image.crop((left, top, right, bottom))
chart.save("chart.png")
print("✅ Đã lưu ảnh biểu đồ thành chart.png")

# Gửi Telegram
import requests

with open("chart.png", "rb") as photo:
    res = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
        data={"chat_id": CHAT_ID, "caption": "📉 Biểu đồ thanh lý BTC từ Coinglass"},
        files={"photo": photo}
    )
    print("📤 Gửi ảnh:", res.status_code, res.text)
