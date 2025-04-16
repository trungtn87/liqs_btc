import os
import requests
from playwright.sync_api import sync_playwright

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

url = "https://www.coinglass.com/vi/pro/futures/LiquidationHeatMap"
screenshot_path = "btc_chart.png"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url, timeout=60000)
    page.wait_for_timeout(8000)
    page.screenshot(path=screenshot_path, full_page=True)
    browser.close()

print("✅ Screenshot captured.")

# Kiểm tra file đã tồn tại chưa và dung lượng
if not os.path.exists(screenshot_path):
    print("❌ Lỗi: File ảnh không tồn tại.")
else:
    print("📸 File ảnh tồn tại.")
    print("📏 Kích thước:", os.path.getsize(screenshot_path), "bytes")

    with open(screenshot_path, 'rb') as photo:
        response = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
            data={"chat_id": CHAT_ID, "caption": "Biểu đồ thanh lý BTC từ Coinglass 📉"},
            files={"photo": photo}
        )

        print("📤 Đang gửi ảnh đến Telegram...")
        print("🔁 Status code:", response.status_code)
        print("📦 Response text:", response.text)
