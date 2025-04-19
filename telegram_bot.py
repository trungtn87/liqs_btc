

import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from send_chart import capture_chart_and_send
from dotenv import load_dotenv
from fastapi import FastAPI
from telegram.ext import WebhookHandler

load_dotenv()

BOT_TOKEN = os.getenv("7424883795:AAEYhQX61gfReKem4AT13--hgxs7ZUOnXSY")
WEBHOOK_URL = os.getenv("https://liqs-btc.onrender.com")  # Ví dụ: https://liqs-btc.onrender.com/webhook

app = FastAPI()  # FastAPI để Render hiểu

telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Chào bạn! Gửi /chart để nhận ảnh nhé.")

async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📸 Đang xử lý, đợi tí nhé...")
    await capture_chart_and_send()
    await update.message.reply_text("✅ Ảnh đã được gửi!")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("chart", chart))

# Webhook endpoint
@app.post("/webhook")
async def telegram_webhook(update: dict):
    update_obj = Update.de_json(update, telegram_app.bot)
    await telegram_app.update_queue.put(update_obj)

# Startup webhook config
@app.on_event("startup")
async def on_startup():
    await telegram_app.bot.set_webhook(url=WEBHOOK_URL)
    print("✅ Webhook đã được thiết lập.")
