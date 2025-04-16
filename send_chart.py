import asyncio
from playwright.sync_api import sync_playwright
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_to_telegram(file_path):
    with open(file_path, 'rb') as photo:
        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
            data={"chat_id": CHAT_ID, "caption": "📊 Biểu đồ thanh lý BTC 24h"},
            files={"photo": photo}
        )
    print(response.text)

def capture_coinglass_screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        print("🔄 Đang mở trang Coinglass...")

        page.goto("https://www.coinglass.com/vi/pro/futures/LiquidationHeatMap", timeout=60000)
        page.wait_for_timeout(10000)

        print("📸 Tìm và nhấn nút chụp ảnh...")
        screenshot_btn = page.query_selector("canvas ~ div button")  # Nút chụp ảnh gần canvas
        if screenshot_btn:
            screenshot_btn.click()
            page.wait_for_timeout(3000)

            print("📥 Tải ảnh từ browser context...")
            with page.expect_download() as download_info:
                page.locator("text=Tải về").click()
            download = download_info.value
            path = download.path()
            file_path = "chart.png"
            download.save_as(file_path)
            print(f"✅ Ảnh đã tải về: {file_path}")
            return file_path
        else:
            print("❌ Không tìm thấy nút chụp ảnh")
            return None

if __name__ == "__main__":
    image_file = capture_coinglass_screenshot()
    if image_file:
        send_to_telegram(image_file)
