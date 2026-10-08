import os
import logging
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8658847499:AAGrpD1rr-9DT5uU7jRI7VJNmBEx41QFxZE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً بك! أرسل لي رابط فيديو من تيك توك وسأقوم بتنزيله لك.")

async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    if "tiktok.com" not in url:
        await update.message.reply_text("يرجى إرسال رابط تيك توك صحيح.")
        return

    status_message = await update.message.reply_text("جاري تحميل الفيديو، انتظر لحظة...")
    output_file = f"tiktok_{update.message.chat_id}.mp4"

    ydl_opts = {
        'outtmpl': output_file,
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await update.message.reply_video(
            video=open(output_file, 'rb'),
            caption="تم التنزيل بنجاح! 🎬"
        )
        await status_message.delete()

    except Exception as e:
        await status_message.edit_text("حدث خطأ أثناء تحميل الفيديو. تأكد من أن الحساب ليس خاصاً أو أرسل رابطاً آخر.")
        print(f"Error details: {e}")

    finally:
        if os.path.exists(output_file):
            os.remove(output_file)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_tiktok))

    print("البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()
