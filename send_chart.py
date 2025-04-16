import time
from playwright.sync_api import sync_playwright
from PIL import Image

URL = "https://www.coinglass.com/vi/pro/futures/LiquidationHeatMap"

def capture_chart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        page = context.new_page()

        print("🔄 Đang mở trang Coinglass...")
        page.goto(URL, timeout=120_000)
        
        time.sleep(15)  # chờ JS render biểu đồ

        print("⏳ Đợi biểu đồ xuất hiện...")
        try:
            chart = page.wait_for_selector(".heat-chart-container", timeout=60_000)
        except:
            print("❌ Không tìm thấy biểu đồ.")
            browser.close()
            return

        print("📸 Đang chụp ảnh...")
        chart.screenshot(path="chart.png")
        print("✅ Đã lưu ảnh chart.png")

        browser.close()

if __name__ == "__main__":
    capture_chart()
