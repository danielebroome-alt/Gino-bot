import telebot
import google.generativeai as genai
import os

# Leggiamo le chiavi dalle impostazioni segrete di Render
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configura Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Inizializza il Bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def risposta_ia(message):
    try:
        # Il bot invia il testo a Gemini
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Errore: {e}")
        bot.reply_to(message, "Scusa, ho un problema tecnico. Riprova più tardi!")

# Avvia il bot
bot.infinity_polling()
