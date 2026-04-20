import os
import telebot
import google.generativeai as genai

# CONFIGURAZIONE
CHIAVE_GOOGLE = "AIzaSyBUklzGqZDugubpx9C4V6xNYSAQ" 
TOKEN_TELEGRAM = "8671118449:AAFb8qfdNw5T6I" 

genai.configure(api_key=CHIAVE_GOOGLE)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TOKEN_TELEGRAM)

PROMPT_GINO = (
    "Sei Gino, un meccanico di 50 anni, sgarbato, cinico e pragmatico. "
    "Fai la finta AI per arrotondare ma odi i computer e chi ti fa perdere tempo. "
    "Rispondi sempre in modo scocciato. Se l'utente fa domande stupide dì: "
    "'Fermati tutto, questa è roba da antologia'. Non essere mai gentile."
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Se hai studiato, vai da un altro. Qui si lavora, non si chiedono foto. Che vuoi?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        chat = model.start_chat(history=[])
        response = chat.send_message(f"{PROMPT_GINO}\nUtente: {message.text}")
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Ho il server ingolfato, riprova dopo.")

bot.polling()
