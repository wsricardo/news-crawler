import telebot
import json

token = 'token'

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")
@bot.message_handler( commands=['news', 'help'] )
def send_news(message):
    datares = None
    with open('noticias.json', 'r') as fl:
        datares = fl.read()
        fl.close()
    out = json.loads(datares)
    #print(out[0])
    import random
    out = random.sample(out, k=3)
    for i in out:
        bot.reply_to(message, i['title']+'\n'+i['href'])
    
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text
    test = lambda text: 'Noticia' in text or 'noticia' in text or 'Notícia' in text or 'Noticias' in text or 'noticias' in text or 'Notícias' in text
    
    if test(text):
        datares = None
        with open('noticias.json', 'r') as fl:
            datares = fl.read()
            fl.close()
        out = json.loads(datares)
        #print(out[0])
        import random
        out = random.sample(out, k=3)
        for i in out:
            bot.reply_to(message, i['title']+'\n'+i['href'])
    else:
        bot.reply_to(message, message.text)


bot.infinity_polling()
