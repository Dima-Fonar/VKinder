from random import randrange
from orm import *
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from community_token import TOKEN_GROUP
from vk_requests import get_user_info, get_user_search, get_photos

db = ORM()

vk = vk_api.VkApi(token=TOKEN_GROUP)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    """
    функция отправки текстовых сообщений пользователю
    :param user_id: VK id пользователя которуму отправляем сообщение
    :param message: текс сообщения
    :return:
    """
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})


def write_msg_attachment(user_id, message, attachment):
    """
    функция отправки сообщений с вложенными фото пользователю
    :param user_id: VK id пользователя которуму отправляем сообщение
    :param message: текс сообщения
    :param attachment: медиавложения к личному сообщению, перечисленные через запятую.
    :return:
    """
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7), 'attachment': attachment})


def greeting(user_id):
    """
    функция получает от API VK имя пользователя который общается с ботом
    :param user_id:VK id пользователя
    :return: Имя пользователя
    """
    user_fullname = vk.method("users.get", {"user_ids": user_id})
    fullname = user_fullname[0]["first_name"]
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

                user = get_user_search(user_info)
                for i in user:
                    user_id_to_db = i[0]
                    db.create_tables()
                    if not db.search_id(user_id_to_db):
                        db.add_user(user_id_to_db, event.user_id)
                        photo = get_photos(user_id_to_db)
                        write_msg_attachment(event.user_id,f'https://vk.com/id{user_id_to_db}', photo)




