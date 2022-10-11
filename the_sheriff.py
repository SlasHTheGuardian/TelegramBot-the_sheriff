import telebot
from the_sheriff_text_processing import *
from the_sheriff_voice_processing import *


TOKEN = '5604845141:AAGr6654SGj77dS9kC5qJaPuIzOza2Xix1I'
murl = f'https://api.telegram.org/bot{TOKEN}'
bot = telebot.TeleBot(TOKEN)
duel_started = False
gunfight_answer = 0


def random_reaction(n, m, message, phrase, reply=True):
    q = random.randint(1, m)
    if q <= n:
        if reply:
            bot.reply_to(message, phrase)
        else:
            bot.send_message(message.chat.id, phrase)


with open("data/phrases.json", "r", encoding='utf-8') as phrases:
    phrases = json.load(phrases)


@bot.message_handler(content_types=['text'])
def echo(message):

    def analysing_msg():
        global duel_started, gunfight_answer
        duel_started, gunfight_answer = duel(bot, message, duel_started, gunfight_answer)
        print(duel_started, gunfight_answer)
        # current_date = datetime.datetime.now().date()
        current_time = datetime.datetime.now().time()
        rules(bot, message)
        add_player_info(bot, message)
        tag_everyone(bot, message, current_time)
        check_person(bot, message)
        remove_player_info(bot, message)
        show_statistics(bot, message)

    analysing_msg()


@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    time.sleep(1)
    phrase = random.choice(phrases["phrase_photo_dict"])
    random_reaction(1, 7, message, phrase)


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    voice_to_text(bot, message)


bot.polling(timeout=60)
