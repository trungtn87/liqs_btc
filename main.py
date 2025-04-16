import requests
import os

# Lấy token và chat ID từ biến môi trường GitHub Actions
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# URL chụp màn hình biểu đồ
IMG_URL = 'https://image.thum.io/get/width/1920/https://www.coinglass.com/vi/pro/futures/LiquidationHeatMap'

# Tải ảnh về
img_data = requests.get(IMG_URL).content
with open('btc_chart.png', 'wb') as handler:
    handler.write(img_data)

# Gửi ảnh qua Telegram
with open('btc_chart.png', 'rb') as photo:
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
        data={"chat_id": CHAT_ID, "caption": "📊 Biểu đồ thanh lý BTC"},
        files={"photo": photo}
    )
