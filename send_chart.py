import asyncio
from playwright.sync_api import sync_playwright
import requests
import os

TELEGRAM_BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("CHAT_ID")

def send_photo_to_telegram(image_path):
    print("📤 Đang gửi ảnh đến Telegram...")
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    with open(image_path, "rb") as img:
        files = {"photo": img}
        data = {"chat_id": TELEGRAM_CHAT_ID}
        response = requests.post(url, files=files, data=data)
        print(f"🔁 Status code: {response.status_code}")
        print(f"📦 Response text: {response.text}")
        return response.status_code == 200

def main():
    with sync_playwright() as p:
        print("🔄 Đang mở trang Coinglass...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto("https://www.coinglass.com/vi/pro/futures/LiquidationHeatMap", timeout=60000)
        page.wait_for_timeout(8000)  # đợi page render biểu đồ và nút chụp

        print("📸 Tìm và nhấn nút có biểu tượng...")

        # Tìm tất cả nút, nhấn nút có SVG đầu tiên
        buttons = page.locator("div button")
        clicked = False
        for i in range(buttons.count()):
            btn = buttons.nth(i)
            if btn.locator("svg").count() > 0:
                btn.click()
                clicked = True
                print("✅ Đã nhấn nút chụp ảnh.")
                break

        if not clicked:
            print("❌ Không tìm thấy nút chụp ảnh có svg.")
            browser.close()
            return

        page.wait_for_timeout(5000)  # Đợi ảnh render xong

        # Tìm thẻ ảnh sau khi nhấn nút
        print("🔍 Đang tìm ảnh đã render...")
        try:
            img_element = page.locator("img").first
            img_url = img_element.get_attribute("src")
            if img_url.startswith("data:image"):
                print("❌ Ảnh render dạng base64, không tải được.")
                return
            print(f"🌐 URL ảnh: {img_url}")

            # Tải ảnh về
            img_data = requests.get(img_url).content
            with open("chart.png", "wb") as f:
                f.write(img_data)
            print("✅ Đã lưu ảnh thành chart.png")

            # Gửi Telegram
            send_photo_to_telegram("chart.png")
        except Exception as e:
            print("❌ Không tìm thấy ảnh hoặc lỗi khi tải ảnh:", e)

        browser.close()

if __name__ == "__main__":
    main()
