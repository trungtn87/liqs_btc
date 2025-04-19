from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import subprocess
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")  # hoặc gõ thẳng token ở đây
CHART_SCRIPT_PATH = "send_chart.py"

async def chart_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Đang tạo ảnh từ Coinglass, xin chờ...")

    try:
        # Gọi script chụp ảnh và gửi Telegram
        subprocess.run(["python3", CHART_SCRIPT_PATH], check=True)
    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f"❌ Lỗi khi chạy script: {e}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Có lỗi xảy ra: {e}")

    # Không cần gửi ảnh trong bot này, vì ảnh đã được gửi trong script rồi

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("chart", chart_handler))

    print("🤖 Bot Telegram đã sẵn sàng...")
    app.run_polling()
