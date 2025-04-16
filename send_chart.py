from playwright.sync_api import sync_playwright
from PIL import Image
import os
import requests

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto("https://www.coinglass.com/vi/pro/futures/LiquidationHeatMap", timeout=60000)

    # Đợi biểu đồ hiện ra (tăng timeout nếu mạng yếu)
    page.wait_for_selector(".heat-chart-container", timeout=60000)

    # Lấy phần tử biểu đồ và chụp riêng nó
    chart_element = page.locator(".heat-chart-container")
    chart_element.screenshot(path="chart.png")

    print("✅ Đã lưu ảnh biểu đồ thành chart.png")
    browser.close()

# Gửi ảnh Telegram
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
with open("chart.png", "rb") as photo:
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
        data={"chat_id": CHAT_ID, "caption": "📊 Biểu đồ thanh lý BTC từ Coinglass"},
        files={"photo": photo}
    )
