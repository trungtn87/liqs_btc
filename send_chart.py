import time
from playwright.sync_api import sync_playwright
from PIL import Image
import requests
import os

URL = "https://www.coinglass.com/vi/pro/futures/LiquidationHeatMap"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def capture_chart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        page = context.new_page()

        print("🔄 Đang mở trang Coinglass...")
        page.goto(URL, timeout=120_000)
        time.sleep(15)  # cho JS render biểu đồ

        print("⏳ Đợi biểu đồ xuất hiện...")
        try:
            chart = page.wait_for_selector(".heat-chart-container", timeout=60_000)
        except:
            print("❌ Không tìm thấy biểu đồ.")
            browser.close()
            return False

        print("📸 Chụp ảnh...")
        chart.screenshot(path="chart.png")
        print("✅ Đã lưu ảnh chart.png")
        browser.close()
        return True

def send_to_telegram():
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ Thiếu biến môi trường BOT_TOKEN hoặc CHAT_ID")
        return

    with open("chart.png", "rb") as img:
        print("📤 Đang gửi ảnh lên Telegram...")
        resp = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
            data={"chat_id": CHAT_ID},
            files={"photo": img}
        )
    if resp.status_code == 200:
        print("✅ Gửi ảnh thành công!")
    else:
        print(f"❌ Lỗi khi gửi ảnh: {resp.text}")

if __name__ == "__main__":
    if capture_chart():
        send_to_telegram()
