import json


class Citizen:
    def __init__(self, name, username, id, city_id):
        self.name = name
        self.username = username
        self.id = id
        self.city_id = city_id  # chat_id is equal to "city"
        self.statistics_gunfight = {
            "wins": 0,
            "misses": 0
        }


citizens_info_path = 'data/citizens_info.json'


def load_citizens_info():
    with open(citizens_info_path, "r", encoding='utf-8') as citizens_info_db:
        citizens_info = json.load(citizens_info_db)
    return citizens_info


def save_citizens_info(citizens_info):
    with open(citizens_info_path, "w", encoding='utf-8') as citizens_info_db:
        json.dump(citizens_info, citizens_info_db, sort_keys=True, indent=4)


def load_personal_info(person_id, city_id):
    citizens_info = load_citizens_info()
    for item in citizens_info:
        if item["id"] == person_id and item["city_id"] == city_id:
            return item


def save_personal_info(person):
    citizens_info = load_citizens_info()
    founded = False
    for item in citizens_info:
        if item["id"] == person["id"] and item["city_id"] == person["city_id"]:
            founded = True
            citizens_info.remove(item)
            citizens_info.append(person)
            save_citizens_info(citizens_info)
            break
    if not founded:
        print("Гражданин не найден")
