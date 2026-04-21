import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
import google.generativeai as genai

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# API Keys
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Usiamo il modello "gemini-pro" che è il più stabile per le librerie attuali
model = genai.GenerativeModel('gemini-1.5-flash-latest')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text
        # Prompt ridotto all'osso per evitare blocchi
        prompt = f"Sei Gino, un meccanico brusco. Rispondi a: {user_text}"
        response = model.generate_content(prompt)
        
        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("Gino mugugna ma non parla (Nessuna risposta).")
            
    except Exception as e:
        # Se c'è un errore, Gino ci dirà esattamente QUALE su Telegram
        await update.message.reply_text(f"Errore tecnico: {str(e)[:100]}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Che vuoi? Sono Gino. Scrivi e non rompermi i bulloni.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.run_polling()
