from playwright.sync_api import sync_playwright
from PIL import Image
import os
import time
import requests

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    print("🔁 Mở trang Coinglass...")
    page.goto("https://www.coinglass.com/vi/pro/futures/LiquidationHeatMap", timeout=60000)

    print("⏳ Đợi trang load thêm 10 giây...")
    page.wait_for_timeout(10000)  # đợi thêm để JS render biểu đồ

    try:
        print("🔍 Tìm biểu đồ...")
        chart = page.locator(".heat-chart-container")
        chart.screenshot(path="chart.png")
        print("✅ Đã chụp riêng biểu đồ!")
    except Exception as e:
        print("⚠️ Không tìm được biểu đồ, fallback toàn màn hình.")
        page.screenshot(path="chart.png")

    browser.close()

# Gửi ảnh lên Telegram
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
with open("chart.png", "rb") as photo:
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
        data={"chat_id": CHAT_ID, "caption": "📊 Biểu đồ thanh lý BTC từ Coinglass"},
        files={"photo": photo}
    )
