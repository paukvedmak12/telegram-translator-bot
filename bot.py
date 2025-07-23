from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import aiohttp
from config import TELEGRAM_BOT_TOKEN, DEEPL_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! Send me text in Latvian, and I'll translate it to English using DeepL."
    )

async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text:
        await update.message.reply_text("Please send some text for translation.")
        return

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api-free.deepl.com/v2/translate",
                data={
                    "auth_key": DEEPL_API_KEY,
                    "text": text,
                    "source_lang": "LV",
                    "target_lang": "EN"
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                timeout=10
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    translation = result["translations"][0]["text"]
                else:
                    error_text = await response.text()
                    translation = f"DeepL API error: {response.status} — {error_text}"
    except Exception as e:
        translation = f"Translate Error: {e}"

    await update.message.reply_text(translation)

def main():
    print("🤖 Bot is running...")
    print("🔑 Ключ DeepL:", DEEPL_API_KEY)

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_text))
    app.run_polling()

if __name__ == "__main__":
    main()
