import telebot
import speech_recognition as sr
from the_sheriff_text_processing import *
import os


TOKEN = '5604845141:AAGr6654SGj77dS9kC5qJaPuIzOza2Xix1I'
murl = f'https://api.telegram.org/bot{TOKEN}'
bot = telebot.TeleBot(TOKEN)
r = sr.Recognizer()
language = 'ru_RU'
duel_started = False
gunfight_answer = 0


def random_reaction(n, m, message, phrase, reply=True):
    q = random.randint(1, m)
    if q <= n:
        if reply:
            bot.reply_to(message, phrase)
        else:
            bot.send_message(message.chat.id, phrase)


with open("phrases.json", "r",  encoding='utf-8') as phrases:
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

    analysing_msg()


@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    time.sleep(1)
    phrase = random.choice(phrases["phrase_photo_dict"])
    random_reaction(1, 7, message, phrase)


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    def recognise(filename):
        with sr.AudioFile(filename) as source:
            audio_text = r.listen(source)
            try:
                text = r.recognize_google(audio_text, language=language)
                print('Converting audio transcripts into text ...')
                print(text)
                return text
            except:
                print('Sorry.. run again...')
                return "Sorry.. run again..."
    file_name_ogg = "./voice/voicemessage.ogg"
    file_name_wav = "./voice/voicemessage.wav"
    voice_info = bot.get_file(message.voice.file_id)
    voice_data = bot.download_file(voice_info.file_path)
    with open(file_name_ogg, 'wb') as new_file:
        new_file.write(voice_data)
    os.system("ffmpeg -i " + file_name_ogg + "  " + file_name_wav)
    phrase = recognise(file_name_wav)
    bot.reply_to(message, phrase)
    os.remove(file_name_ogg)
    os.remove(file_name_wav)


bot.polling(timeout=60)
