import requests
import json
import time
from datetime import datetime
from pprint import pprint

with open('token.txt', 'r') as file:
    token = file.read().strip()

class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version='5.131'):
        self.params = {
            'access_token': token,
            'v': version
        }

    def get_photos_allinfo(self):
        get_photos_url = self.url + 'photos.get'
        get_photos_params = {
            'album_id': 'profile',
            'extended': '1'
        }
        res = requests.get(get_photos_url, params={**self.params, **get_photos_params}).json()
        return res

    def sort_photos_info(self):
        photos_info = {}
        res = self.get_photos_allinfo()
        for item in res['response']['items']:
            photos_info[item['id']] = {}
            photos_info[item['id']]['likes'] = item['likes']['count']
            photos_info[item['id']]['date'] = \
                datetime.utcfromtimestamp(int(item['date'])).strftime('%Y-%m-%d %H:%M:%S')
            photos_info[item['id']]['size'] = [item['sizes'][-1]['height'], item['sizes'][-1]['width']]
            photos_info[item['id']]['url'] = item['sizes'][-1]['url']
        return photos_info

    def download_photos(self):
        photos_info = self.sort_photos_info()
        result_file = {}
        for photo in photos_info:
            pprint(str(photo['likes']))
            if photo['likes'] not in result_file:
                result_file[f'{photo["likes"]}'] = f'{photo[size][0]}x{photo[size][1]}'
        return result_file



NewUser = VkUser(token)
info = NewUser.sort_photos_info()
NewUser.download_photos()
# pprint(info)







