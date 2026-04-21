import telebot
import google.generativeai as genai
import os

# Leggiamo le chiavi dalle impostazioni
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configura Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Inizializza il Bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def risposta_ia(message):
    try:
        # Il bot invia il testo a Gemini
        response = model.generate_content(message.text)
        
        # Controlliamo se Gemini ha prodotto del testo
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Gemini non ha saputo rispondere a questo messaggio.")
            
    except Exception as e:
        print(f"Errore: {e}")
        # Ti invia l'errore preciso su Telegram così lo leggiamo lì!
        bot.reply_to(message, f"Errore tecnico: {e}")

# Avvia il bot
bot.infinity_polling()
