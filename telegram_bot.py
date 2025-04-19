import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from send_chart import capture_chart_and_send
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 8443))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Chào bạn! Gửi /chart để nhận ảnh nhé.")

async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📸 Đang xử lý, đợi tí nhé...")
    await capture_chart_and_send()
    await update.message.reply_text("✅ Ảnh đã được gửi!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("chart", chart))

    print("🤖 Bot Telegram đang chạy qua webhook...")

    # Chạy webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{BOT_TOKEN}"
    )
