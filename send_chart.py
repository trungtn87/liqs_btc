import asyncio
from playwright.async_api import async_playwright
from PIL import Image
import requests
import os

async def capture_chart():
    print("🔄 Đang mở trang Coinglass...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        await page.goto("https://www.coinglass.com/vi/pro/futures/LiquidationHeatMap", timeout=60000)
        print("⏳ Đợi biểu đồ hiển thị...")
        await page.wait_for_timeout(10000)  # Chờ 10s cho chắc

        await page.screenshot(path="screenshot.png", full_page=True)
        await browser.close()

    # Crop theo tọa độ cố định (đã đo chuẩn tay từ ảnh mẫu)
    print("✂️ Đang crop ảnh...")
    image = Image.open("screenshot.png")
    left = 120
    top = 280
    right = 1820
    bottom = 950
    chart = image.crop((left, top, right, bottom))
    chart.save("chart.png")
    print("✅ Đã lưu ảnh chart.png")

def send_telegram():
    print("📤 Gửi ảnh về Telegram...")
    TOKEN = os.environ["BOT_TOKEN"]
    CHAT_ID = os.environ["CHAT_ID"]

    with open("chart.png", "rb") as photo:
        res = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
            data={"chat_id": CHAT_ID, "caption": "🔥 Biểu đồ thanh lý BTC từ Coinglass"},
            files={"photo": photo}
        )
    print(f"✅ Đã gửi: {res.status_code}, {res.text}")

async def main():
    await capture_chart()
    send_telegram()

if __name__ == "__main__":
    asyncio.run(main())
