import os
import asyncio
from pathlib import Path
import requests
from playwright.async_api import async_playwright

COINGLASS_URL = "https://www.coinglass.com/vi/pro/futures/LiquidationHeatMap"
DOWNLOAD_DIR = Path("./screenshots")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

async def capture_chart_and_send():
    DOWNLOAD_DIR.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()

        print("🔄 Đang mở trang Coinglass...")
        await page.goto(COINGLASS_URL)
        await page.wait_for_timeout(5000)

        print("🔁 Đang tìm nút 'Ký hiệu'...")
        await page.wait_for_selector("button", timeout=10000)
        symbol_button = page.locator("button", has_text="Ký hiệu").first
        if await symbol_button.is_visible():
            print("🟢 Nhấn nút 'Ký hiệu'...")
            await symbol_button.click()
            await page.wait_for_timeout(3000)

        print("📸 Tìm và nhấn nút chụp ảnh SVG...")
        buttons = await page.query_selector_all("button")
        download = None
        for btn in buttons:
            inner_html = await btn.inner_html()
            if "<svg" in inner_html.lower():
                try:
                    async with page.expect_download(timeout=10000) as download_info:
                        await btn.click()
                    download = await download_info.value
                    break
                except:
                    continue

        if not download:
            print("❌ Không tìm thấy nút chụp ảnh hoặc không thể click.")
            await browser.close()
            return

        file_path = DOWNLOAD_DIR / "chart.png"
        await download.save_as(file_path)

        print(f"📤 Gửi ảnh {file_path} lên Telegram...")
        with open(file_path, "rb") as img:
            response = requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                data={"chat_id": CHAT_ID},
                files={"photo": img}
            )

        if response.status_code == 200:
            print("✅ Đã gửi thành công!")
            os.remove(file_path)
        else:
            print(f"❌ Gửi ảnh thất bại: {response.status_code}, {response.text}")

        await browser.close()
