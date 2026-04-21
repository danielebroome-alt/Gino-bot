import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
import google.generativeai as genai

# Configurazione Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Configurazione API Keys
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        # Prompt per dare il carattere a "Gino ignorante"
        prompt = f"Rispondi come se fossi un meccanico di 60 anni, ignorante, brusco e sarcastico: {user_text}"
        response = model.generate_content(prompt)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Errore: {e}")
        await update.message.reply_text("Non mi va di rispondere ora, lasciami stare.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Che vuoi? Sono Gino. Scrivi e non rompermi i bulloni.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Gino è acceso...")
    application.run_polling()
