
from playwright.sync_api import sync_playwright
import requests
import os

# ==== THÔNG SỐ BẠN CẦN CẤU HÌNH ====
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # hoặc thay bằng chuỗi token trực tiếp nếu muốn
CHAT_ID = os.environ.get("CHAT_ID")      # hoặc thay bằng số chat_id

URL = "https://www.coinglass.com/vi/pro/futures/LiquidationHeatMap"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    print("🔄 Đang mở trang Coinglass...")
    page.goto(URL, timeout=60000)

    print("⏳ Đợi biểu đồ hiển thị...")
    page.wait_for_timeout(10000)

    # Cuộn xuống một chút nếu cần (trong trường hợp biểu đồ không hiện ngay)
    page.mouse.wheel(0, 500)
    page.wait_for_timeout(3000)

    # Tìm phần tử biểu đồ chính xác
    chart_elem = page.query_selector(".heat-chart-container")
    if chart_elem:
        chart_elem.screenshot(path="chart.png")
        print("✅ Đã chụp biểu đồ thành công")
    else:
        print("❌ Không tìm thấy phần tử biểu đồ!")
        browser.close()
        exit()

    browser.close()

# 📤 Gửi ảnh qua Telegram
if BOT_TOKEN and CHAT_ID:
    with open("chart.png", "rb") as photo:
        res = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
            data={"chat_id": CHAT_ID, "caption": "📉 Biểu đồ thanh lý BTC từ Coinglass"},
            files={"photo": photo}
        )
        print("📤 Gửi ảnh:", res.status_code, res.text)
else:
    print("⚠️ Thiếu BOT_TOKEN hoặc CHAT_ID, không gửi được Telegram.")
