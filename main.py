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

# Configurazione del modello con filtri disattivati per evitare blocchi
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings={
        "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
    }
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        # Prompt per Gino
        prompt = f"Tu sei Gino, un meccanico anziano, stanco, brusco e sarcastico. Rispondi a questo: {user_text}"
        response = model.generate_content(prompt)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Errore: {e}")
        await update.message.reply_text("Ho finito il grasso per i gomiti, ripassa dopo.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Che vuoi? Sono Gino. Scrivi e non rompermi i bulloni.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.run_polling()
