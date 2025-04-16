from playwright.sync_api import sync_playwright
from PIL import Image
import requests
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto("https://www.coinglass.com/vi/pro/futures/LiquidationHeatMap", timeout=60000)
    
    # Chờ biểu đồ xuất hiện
    page.wait_for_selector(".heat-chart-container", timeout=30000)

    # Chụp toàn màn hình
    page.screenshot(path="full.png")

    # Lấy vị trí và kích thước biểu đồ
    box = page.locator(".heat-chart-container").bounding_box()
    if box:
        image = Image.open("full.png")
        cropped = image.crop((box["x"], box["y"], box["x"] + box["width"], box["y"] + box["height"]))
        cropped.save("chart.png")
        print("✅ Đã lưu chart.png")

        # Gửi Telegram
        with open("chart.png", "rb") as photo:
            response = requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                data={"chat_id": CHAT_ID, "caption": "📉 Biểu đồ thanh lý BTC"},
                files={"photo": photo}
            )
            print(response.status_code, response.text)
    else:
        print("❌ Không tìm thấy biểu đồ.")

    browser.close()
