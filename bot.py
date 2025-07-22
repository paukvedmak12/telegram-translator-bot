from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import aiohttp
from config import TELEGRAM_BOT_TOKEN, TILDE_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me text in Latvian, and i translate it to english.")

async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.letsmt.eu/Translate",
                json={
                    "text": text,
                    "sourceLanguage": "lv",
                    "targetLanguage": "en",
                    "system": "generic"
                },
                headers={"Authorization": f"Bearer {TILDE_API_KEY}"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    translation = result.get("translation", "Перевод не найден.")
                else:
                    translation = f"Error: {response.status}"
    except Exception as e:
        translation = f"Translate Error: {e}"

    await update.message.reply_text(translation)

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_text))
    app.run_polling()

if __name__ == "__main__":
    main()
