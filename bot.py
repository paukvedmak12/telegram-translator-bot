# bot.py

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import aiohttp
from config import TELEGRAM_BOT_TOKEN, TILDE_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне текст, и я переведу его с латышского на английский.")

async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    try:
        response = aiohttp.post(
            "https://api.letsmt.eu/Translate",
            json={
                "text": text,
                "sourceLanguage": "lv",
                "targetLanguage": "en",
                "system": "generic"
            },
            headers={"Authorization": f"Bearer {TILDE_API_KEY}"}
        )

        if response.status_code == 200:
            translation = response.json().get("translation", "Перевод не найден.")
        else:
            translation = f"Ошибка: {response.status_code}"

    except Exception as e:
        translation = f"Произошла ошибка: {e}"

    await update.message.reply_text(translation)

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_text))
    app.run_polling()

if __name__ == "__main__":
    main()
