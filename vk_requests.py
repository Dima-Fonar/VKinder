from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from community_token import TOKEN_GROUP

vk = vk_api.VkApi(token=TOKEN_GROUP)
longpoll = VkLongPoll(vk)


def get_user_info(user_id):
    all_info = vk.method('users.get', {'user_id': user_id, 'fields': 'bdate,sex,city,relation'})
    all_info = all_info[0]
    user_info = {'id': user_id}
    if 'bdate' in all_info:
        user_info['bdate'] = all_info['bdate']
    if 'sex' in all_info:
        user_info['sex'] = all_info['sex']
    if 'city' in all_info:
        user_info['city_id'] = all_info['city']['id']
        user_info['city_title'] = all_info['city']['title']
    if 'relation' in all_info:
        user_info['relation'] = all_info['relation']
    return user_info


def get_user_search():
    ...
