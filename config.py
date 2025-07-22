# config.py

# Configuration settings for the Telegram Translator Bot
from dotenv import load_dotenv
import os
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TILDE_API_KEY = os.getenv("TILDE_API_KEY")

# Supported languages
SUPPORTED_LANGUAGES = ["en", "es", "fr", "de", "ru", "zh"]

# Default language
DEFAULT_LANGUAGE = "en"