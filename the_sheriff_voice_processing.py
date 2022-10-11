import speech_recognition as sr
import os
import random
import json

language = 'ru_RU'
r = sr.Recognizer()
with open("data/phrases.json", "r", encoding='utf-8') as phrases:
    phrases = json.load(phrases)


def voice_to_text(bot, message):
    file_name_ogg = "./voice/voicemessage.ogg"
    file_name_wav = "./voice/voicemessage.wav"
    voice_info = bot.get_file(message.voice.file_id)
    voice_data = bot.download_file(voice_info.file_path)
    with open(file_name_ogg, 'wb') as new_file:
        new_file.write(voice_data)
    os.system("ffmpeg -y -i " + file_name_ogg + "  " + file_name_wav)
    with sr.AudioFile(file_name_wav) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text, language=language)
            phrase = random.choice(phrases["voice_handling"]) + '"' + text + '"'
        except:
            phrase = random.choice(phrases["voice_handling_error"])
    bot.reply_to(message, phrase)
