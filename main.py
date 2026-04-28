import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import google.generativeai as genai

# Logging (serve per vedere errori)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Configurazione GEMINI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

# Funzione che risponde ai messaggi
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text

        response = model.generate_content(user_text)

        await update.message.reply_text(response.text)

    except Exception as e:
        logging.error(f"Errore: {e}")
        await update.message.reply_text("Si è rotto qualcosa, capo. Riprova tra poco.")

# Avvio del bot
def main():
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

    app = ApplicationBuilder().token(telegram_token).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
