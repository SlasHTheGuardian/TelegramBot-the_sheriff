from the_citizen import *
import re
import datetime
import random
import time


with open("data/phrases.json", "r", encoding='utf-8') as phrases:
    phrases = json.load(phrases)


def is_in_the_city(message):
    sender_id = message.from_user.id
    city_id = message.chat.id
    citizens_info = load_citizens_info()
    for item in citizens_info:
        if item["id"] == sender_id and item["city_id"] == city_id:
            return True
    return False


def is_mentioned(message):
    msg = message.text.lower()
    name_regular = 'господин шериф|шериф|господин офицер|офицер'
    mention = re.match(name_regular, msg)
    if mention:
        return True
    else:
        return False


def is_night(current_time):
    silent_time_start = datetime.time(0, 0, 0, 0)  # 0:00:00
    silent_time_end = datetime.time(11, 0, 0, 0)  # 11:00:00
    if silent_time_start < current_time < silent_time_end:
        return True
    else:
        return False


def check_person(bot, message):
    if is_mentioned(message) and not is_in_the_city(message):
        phrase = random.choice(phrases["not_the_citizen"])
        bot.reply_to(message, phrase)


def add_player_info(bot, message):
    msg = message.text.lower()
    sender_id = message.from_user.id
    sender_username = message.from_user.username
    sender_name = message.from_user.first_name
    city_id = message.chat.id
    if is_mentioned(message) and re.search("запишите меня", msg):
        citizens_info = load_citizens_info()
        sender_in_db_this_city = False
        for item in citizens_info:
            if item["id"] == sender_id and item["city_id"] == city_id:
                sender_in_db_this_city = True
                break
        if sender_in_db_this_city:
            phrase_known_person = random.choice(phrases["phrase_known_person"])
            phrase = sender_name + ", " + phrase_known_person
        else:
            new_citizen = Citizen(sender_name, sender_username, sender_id, city_id)
            citizens_info.append(new_citizen.__dict__)
            save_citizens_info(citizens_info)
            phrase_new_person = random.choice(phrases["phrase_new_person"])
            phrase = sender_name + ", " + phrase_new_person
        bot.send_message(message.chat.id, phrase)


def remove_player_info(bot, message):
    msg = message.text.lower()
    sender_id = message.from_user.id
    city_id = message.chat.id
    if is_mentioned(message) and re.search("уничтожьте мои данные", msg) and is_in_the_city(message):
        phrase = random.choice(phrases["removing_the_citizen"])
        bot.reply_to(message, phrase)
        citizens_info = load_citizens_info()
        for item in citizens_info:
            if item["id"] == sender_id and item["city_id"] == city_id:
                citizens_info.remove(item)
        save_citizens_info(citizens_info)


def rules(bot, message):
    msg = message.text.lower()
    if is_mentioned(message) and is_in_the_city(message):
        rules_regular = "правила спортивной мафии"
        rules_in_message = re.search(rules_regular, msg)
        if rules_in_message:
            phrase = "Вы можете изучить правила спортивной мафии тут: " + phrases["rules_link"]
            bot.reply_to(message, phrase)


def tag_everyone(bot, message, current_time):
    msg = message.text.lower()
    city_id = message.chat.id
    if is_mentioned(message) and is_in_the_city(message) and re.search("общий сбор", msg):
        if is_night(current_time):
            phrase = random.choice(phrases["phrase_silent_time"])
            bot.reply_to(message, phrase)
        else:
            citizens_list = []
            citizens_info = load_citizens_info()
            for item in citizens_info:
                if item["city_id"] == city_id:
                    citizens_list.append(item["username"])
            phrase = "Город, внимание!\nОбщий сбор!\n---------------\n"
            for item in citizens_list:
                phrase += "@" + item + " "
            phrase += "\n---------------\nВнимание!"
            bot.send_message(message.chat.id, phrase)


def show_statistics(bot, message):
    msg = message.text.lower()
    sender_id = message.from_user.id
    city_id = message.chat.id
    if is_mentioned(message) and is_in_the_city(message):
        statistics_regular = "мои данные"
        statistics_in_message = re.search(statistics_regular, msg)
        if statistics_in_message:
            citizens_info = load_citizens_info()
            for item in citizens_info:
                if item["id"] == sender_id and item["city_id"] == city_id:
                    statistics_gunfight = item["statistics_gunfight"]
                    phrase = "Ваши данные:" + str(statistics_gunfight)
                    bot.reply_to(message, phrase)


def duel(bot, message, duel_started, gunfight_answer):
    msg = message.text.lower()
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name
    city_id = message.chat.id
    if duel_started:
        if re.search(str("стреляется"), msg) and is_in_the_city(message) and is_mentioned(message):
            player = load_personal_info(sender_id, city_id)
            if re.search(str(gunfight_answer), msg):
                winner_name = sender_name
                bot.send_message(message.chat.id, str(winner_name) + " сострелялся! Поздравляем!")
                player["statistics_gunfight"]["wins"] += 1
                duel_started = False
                gunfight_answer = 0
            else:
                bot.send_message(message.chat.id, str(sender_name) + ", промах!")
                player["statistics_gunfight"]["misses"] += 1
            save_personal_info(player)
            return duel_started, gunfight_answer
        else:
            return duel_started, gunfight_answer
    else:
        if is_mentioned(message) and is_in_the_city(message) and re.search("назначьте перестрелку", msg):
            bot.send_message(message.chat.id,
                             "Внимание, объявляется перестрелка! Господа, зарядите свои пистолеты.")
            plan_first_part = random.randint(0, 3)
            plan_second_part = random.randint(-4, 4)
            msg_rules = bot.send_message(message.chat.id, "Назначается сострел! У вас 5 секунд:")
            time.sleep(0.5)
            if plan_second_part > 0:
                msg_plan = bot.send_message(message.chat.id, phrases["gunfight_plan"][plan_first_part]
                                            + " о ком поговорю +" + str(plan_second_part))
            elif plan_second_part < 0:
                msg_plan = bot.send_message(message.chat.id, phrases["gunfight_plan"][plan_first_part]
                                            + " о ком поговорю " + str(plan_second_part))
            else:
                msg_plan = bot.send_message(message.chat.id, phrases["gunfight_plan"][plan_first_part]
                                            + " о ком поговорю ")
            time.sleep(3)
            bot.delete_message(message.chat.id, msg_plan.message_id)
            time.sleep(0.5)
            bot.delete_message(message.chat.id, msg_rules.message_id)
            bot.send_message(message.chat.id, "Назначается игровая ситуация:")
            time.sleep(1)
            num_of_players_random = random.choice([True, False])
            if num_of_players_random:
                player_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                bot.send_message(message.chat.id, "В городе 10 человек")
            else:
                player_list = [1, 2, 3, 4, 5, 6, 7, 8]
                bot.send_message(message.chat.id, "В городе 8 человек")
            num_of_dead_players = random.randint(0, 4)
            for i in range(num_of_dead_players):
                time.sleep(1)
                position_of_dead_person = random.choice(player_list)
                player_list.remove(position_of_dead_person)
                bot.send_message(message.chat.id, "Игрок №" + str(position_of_dead_person)
                                 + " " + random.choice(phrases["player_status"]) + "!")
            time.sleep(2)
            players_speech = []
            player_list_copy = player_list.copy()
            for i in range(4):
                number_of_picked_person = random.choice(player_list_copy)
                player_list_copy.remove(number_of_picked_person)
                players_speech.append(number_of_picked_person)
            phrase = ""
            gunfight_player_numbers = phrases["gunfight_player_numbers"]
            for item in players_speech:
                style = random.choice(gunfight_player_numbers)
                gunfight_speech = random.choice(phrases["gunfight_speech"])
                number_of_person = style[item - 1]
                phrase += number_of_person + gunfight_speech
            bot.send_message(message.chat.id, phrase)
            if plan_first_part != 3:
                start_player = players_speech[plan_first_part]
            else:
                start_player = players_speech[-1]
            start_player_index = player_list.index(start_player)
            key_position = start_player_index + plan_second_part
            if key_position > len(player_list):
                key_position -= len(player_list)
            elif key_position < 0:
                key_position += len(player_list)
            print("start_player_index:", start_player_index,
                  "key_position:", key_position,
                  "players_speech:", players_speech)
            duel_started = True
            gunfight_answer = player_list[key_position]
            return duel_started, gunfight_answer
        else:
            return duel_started, gunfight_answer
