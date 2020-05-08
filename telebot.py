import telebot
import time
import json
import requests

bot = telebot.TeleBot(<your bot token>)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing? Enter the word you wanna know the meaning of:")


@bot.message_handler(func=lambda message: True)
def dictionary(message):
    app_id = <oxford dictionary api>
    app_key = <oxford dictionay app key>
    word_id = message.text
    url =  "https://od-api.oxforddictionaries.com:443/api/v2/entries/en-us/"+word_id.lower()
    try:

        r = requests.get(url, headers = {'app_id':app_id, 'app_key':app_key})
        dumpfile = json.dumps(r.json())
        response = json.loads(dumpfile)

        etymologies = response['results'][0]['lexicalEntries'][0]['entries'][0]['etymologies']

        definition = response['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions']

        example = response['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['examples'][0]['text']

        text = 'Etymologies: '+etymologies[0]+'\n\nDefinition: '+definition[0]+'\n\nExample: '+example

        bot.reply_to(message, text)

    except:
        bot.reply_to(message, 'Word does not exist. Please check properly')


while True:
    try:
        bot.polling(none_stop=True)
        # ConnectionError and ReadTimeout because of possible timout of the requests library
        # maybe there are others, therefore Exception
    except Exception:
        time.sleep(15)