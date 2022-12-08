from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from community_token import TOKEN_GROUP
from vk_requests import get_user_info



vk = vk_api.VkApi(token=TOKEN_GROUP)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


def greeting(user_id):
    user = vk.method("users.get", {"user_ids": user_id})
    fullname = user[0]["first_name"]
    return fullname


def get_bdate():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                user_bdate = event.text
                return user_bdate


def get_sex():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                user_sex = event.text
                return user_sex


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            if request == "привет":
                write_msg(event.user_id, f"Привет, {greeting(event.user_id)}!\n"
                                         f"Для того чтобы начать искать себе пару введи команду 'start'")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")

            elif request == "start":
                user_info = get_user_info(event.user_id)
                if 'city_id' not in user_info.keys():
                    write_msg(event.user_id,
                              "У тебя в профиле не указан город! Заполни данную информацию и возвращайся!")

                if 'bdate' not in user_info.keys():
                    write_msg(event.user_id, "У тебя в профиле не указана дата рождения! Введи свою дату рождения в формате день.месяц.год.(1.1.1900)")
                    user_bdate = get_bdate()
                    user_info['bdate'] = user_bdate

                if 'sex' not in user_info.keys():
                    write_msg(event.user_id,
                              "У тебя в профиле не указан пол! Введи '1' если ты девушка!\n"
                              "введи '2' если ты парень!)")
                    user_sex = get_sex()
                    user_info['sex'] = user_sex

                print(user_info)
