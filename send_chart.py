import requests

BOT_TOKEN = "7424883795:AAEYhQX61gfReKem4AT13--hgxs7ZUOnXSY"
CHAT_ID = "-4631355369"

IMG_URL = 'https://image.thum.io/get/width/1920/https://www.coinglass.com/vi/pro/futures/LiquidationHeatMap'

# Tải ảnh
img = requests.get(IMG_URL).content
with open('btc.png', 'wb') as f:
    f.write(img)

# Gửi ảnh qua Telegram
with open('btc.png', 'rb') as f:
    requests.post(
        f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto',
        data={'chat_id': CHAT_ID, 'caption': 'Biểu đồ thanh lý BTC từ Coinglass'},
        files={'photo': f}
    )
