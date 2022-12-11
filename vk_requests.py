from random import randrange

import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from community_token import TOKEN_GROUP, TOKEN_USER
import datetime
import time

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


def get_user_search(params_dict):
    result_list = []
    params_for_search = {'access_token': TOKEN_USER, 'v': '5.131', 'sex': params_dict['sex'],'city': str(params_dict['city_id']),
                     'has_photo': 1, 'sort': 0, 'count': 100, 'status': 6, 'offset': randrange(10 * 40),
                     'fields': 'bdate, sex, city, has_photo'}
    if params_for_search['sex'] == '1':
        params_for_search['sex'] = '2'
    else:
        params_for_search['sex'] = '1'

    if 'bdate' in params_dict:
        now_year = datetime.date.today().year
        if params_for_search['sex'] == '1':
            params_for_search['age_from'] = str(now_year - int(params_dict['bdate'][-4:]))
            params_for_search['age_to'] = str(now_year - int(params_dict['bdate'][-4:]) + 3)
        if params_for_search['sex'] == '2':
            params_for_search['age_from'] = str(now_year - int(params_dict['bdate'][-4:]) - 3)
            params_for_search['age_to'] = str(now_year - int(params_dict['bdate'][-4:]))
    result = requests.get('https://api.vk.com/method/users.search', params={**params_for_search}).json()
    for user in result['response']['items']:
        if not user['is_closed']:
            result_list.append([user['id'], f"{user['first_name']} {user['last_name']} https://vk.com/id{user['id']}"])
    return result_list

def get_photos(params_dict):
    likes_photo = []
    for user in params_dict:
        requests_param = {'access_token': TOKEN_USER, 'v': '5.131', 'owner_id': user[0], 'album_id': '-6', 'extended': 1}
        result = requests.get('https://api.vk.com/method/photos.get', params={**requests_param}).json()
        print(result)
        time.sleep(0.15)
    #     for photo in result['response']['items']:
    #         likes_photo.append([photo['id'], photo['owner_id'], photo['likes']['count']])
    # print(likes_photo)
    # likes_photo.sort(key=lambda x: x[2], reverse=True)
    # print(likes_photo)

