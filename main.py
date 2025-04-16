import requests

# Cấu hình Telegram
BOT_TOKEN = "7424883795:AAEYhQX61gfReKem4AT13--hgxs7ZUOnXSY"
CHAT_ID = "-4631355369"

# API chụp màn hình miễn phí
IMG_URL = 'https://image.thum.io/get/width/1920/https://www.coinglass.com/vi/pro/futures/LiquidationHeatMap'

# Tải ảnh từ API
img_data = requests.get(IMG_URL).content
with open('btc_chart.png', 'wb') as handler:
    handler.write(img_data)

# Gửi ảnh qua Telegram
with open('btc_chart.png', 'rb') as photo:
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
        data={"chat_id": CHAT_ID, "caption": "Biểu đồ thanh lý BTC từ Coinglass 📉"},
        files={"photo": photo}
    )
