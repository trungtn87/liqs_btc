from playwright.sync_api import sync_playwright
from PIL import Image
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    
    page.goto("https://www.coinglass.com/vi/pro/futures/LiquidationHeatMap")
    page.wait_for_selector(".heat-chart-container", timeout=60000)

    # Screenshot toàn trang
    page.screenshot(path="fullpage.png")

    # Tìm vùng chứa biểu đồ
    element = page.query_selector(".heat-chart-container")
    box = element.bounding_box()

    # Cắt đúng phần biểu đồ
    image = Image.open("fullpage.png")
    cropped = image.crop((box["x"], box["y"], box["x"] + box["width"], box["y"] + box["height"]))
    cropped.save("chart.png")

    print("✅ Đã lưu ảnh biểu đồ vào chart.png")
