import os
import time
import requests
import glob
from playwright.sync_api import sync_playwright

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_to_telegram(photo_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(photo_path, "rb") as photo:
        response = requests.post(url, data={"chat_id": CHAT_ID}, files={"photo": photo})
    if response.status_code == 200:
        print("✅ Ảnh đã được gửi thành công!")
    else:
        print(f"❌ Gửi ảnh thất bại: {response.status_code}, {response.text}")

def main():
    print("🔄 Đang mở trang Coinglass...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        page.goto("https://www.coinglass.com/vi/pro/futures/LiquidationHeatMap", timeout=60000)
        page.wait_for_timeout(8000)

        print("📸 Tìm và nhấn nút chụp ảnh SVG...")

        try:
            # Tìm tất cả nút SVG, click vào nút có tooltip là "Ảnh chụp màn hình"
            buttons = page.query_selector_all("button")
            found = False
            for button in buttons:
                title = button.get_attribute("aria-label")
                if title and ("chụp" in title.lower() or "screenshot" in title.lower()):
                    with page.expect_download() as download_info:
                        button.click()
                    download = download_info.value
                    download_path = "screenshots/chart.png"
                    download.save_as(download_path)
                    print("⬇️ Đã tải ảnh về:", download_path)
                    found = True
                    break

            if not found:
                print("❌ Không tìm thấy nút chụp ảnh hoặc không thể click.")
                return

        except Exception as e:
            print("❌ Lỗi khi tải ảnh:", e)
            return

        browser.close()

    print("📤 Gửi ảnh screenshots/chart.png lên Telegram...")
    send_to_telegram("screenshots/chart.png")

    try:
        os.remove("screenshots/chart.png")
        print("🧹 Đã xoá ảnh sau khi gửi.")
    except:
        print("⚠️ Không thể xoá ảnh.")

if __name__ == "__main__":
    main()
