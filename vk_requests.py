from random import randrange

import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from params import TOKEN_GROUP, TOKEN_USER, NUMBER_OF_RESULT
import datetime
import time

vk = vk_api.VkApi(token=TOKEN_GROUP)
longpoll = VkLongPoll(vk)


def get_user_info(user_id):
    '''
    функция получает информацию о пользователе из его профиля VK
    :param user_id: id пользователя в VK
    :return:
    '''
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
    '''
    по введенным параметрам осуществляет поиск человека противоположного пола
    :param params_dict:
    :return:
    '''
    result_list = []
    params_for_search = {'access_token': TOKEN_USER, 'v': '5.131', 'sex': params_dict['sex'], 'city': str(params_dict['city_id']),
                     'has_photo': 1, 'sort': 0, 'count': int(NUMBER_OF_RESULT), 'status': 6, 'offset': randrange(10 * 40),
                     'fields': 'bdate, sex, city, has_photo'}
    print(params_for_search['city'])
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

def get_photos(user_id):
    likes_photo = []
    requests_param = {'access_token': TOKEN_USER, 'v': '5.131', 'owner_id': user_id, 'album_id': '-6', 'extended': 1}
    result = requests.get('https://api.vk.com/method/photos.get', params={**requests_param}).json()
    time.sleep(0.15)
    for photo in result['response']['items']:
        likes_photo.append([photo['id'], photo['likes']['count'] + photo['comments']['count']])
    likes_photo.sort(key=lambda x: x[1], reverse=True)
    if len(likes_photo) > 3:
        likes_photo = likes_photo[:3]
    photo_attachment_list = []
    for item in likes_photo:
        photo_attachment_list.append(f'photo{user_id}_{item[0]}')
    attachment_str = ','.join(photo_attachment_list)
    time.sleep(0.35)
    return attachment_str


def get_region(name_region):
    region_list = []
    requests_param = {'access_token': TOKEN_USER, 'v': '5.131', 'country_id': 1, 'q': name_region}
    region = requests.get('https://api.vk.com/method/database.getRegions', params={**requests_param}).json()
    if region['response']['count'] > 1:
        for one_region in region['response']['items']:
            region_list.append(one_region['title'])
        return region_list
    if len(region['response']['items']) == 1:
        return region['response']['items'][0]['id']
    else:
        return f'Я не нашел такой регион, введи заново!'

def get_city(region_id, name_city):
    requests_param = {'access_token': TOKEN_USER, 'v': '5.131', 'country_id': 1, 'q': name_city, 'region_id': region_id}
    city = requests.get('https://api.vk.com/method/database.getCities', params={**requests_param}).json()
    if city['response']['count'] == 0:
        return f'Я не нашел такой город, введи заново!'
    else:
        return city['response']['items'][0]['id']



