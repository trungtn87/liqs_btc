from playwright.sync_api import sync_playwright
import base64
import time
import os
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_to_telegram(image_path):
    bot = Bot(token=BOT_TOKEN)
    with open(image_path, "rb") as f:
        bot.send_photo(chat_id=CHAT_ID, photo=f, caption="📊 Biểu đồ thanh lý BTC (tự động từ Coinglass)")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    print("🔄 Đang truy cập trang Coinglass...")

    # Truy cập trang biểu đồ
    page.goto("https://www.coinglass.com/vi/pro/futures/LiquidationHeatMap", timeout=60000)
    page.wait_for_timeout(10000)  # Đợi toàn bộ trang load

    print("📸 Đang cố gắng chụp ảnh qua UI của Coinglass...")

    # Giả sử nút snapshot có class hoặc text cụ thể (cần kiểm tra cụ thể lại nếu Coinglass có thay đổi)
    # Đây là ví dụ chọn nút có chữ 'Snapshot' (hoặc icon tương ứng)
    snapshot_btn = page.locator("text=Snapshot")
    if snapshot_btn:
        snapshot_btn.click()
        print("🖼 Đã click nút chụp ảnh")
    else:
        print("❌ Không tìm thấy nút Snapshot")
        exit(1)

    # Đợi ảnh được tạo (thường ảnh sẽ render sau vài giây)
    page.wait_for_timeout(5000)

    # Tìm thẻ chứa ảnh base64 (Coinglass dùng canvas -> img)
    img_element = page.query_selector("img[src^='data:image/png;base64']")

    if img_element:
        img_base64 = img_element.get_attribute("src").split(",")[1]
        image_data = base64.b64decode(img_base64)
        with open("chart.png", "wb") as f:
            f.write(image_data)
        print("✅ Đã lưu ảnh về local!")

        # Gửi Telegram
        send_to_telegram("chart.png")
    else:
        print("❌ Không tìm thấy ảnh base64!")

    browser.close()
