import requests
import json
import time
from datetime import datetime
from pprint import pprint
import os

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
        result_dict = {}
        result_file = []
        photos_info = self.sort_photos_info()
        for photo in photos_info:
            if photos_info[photo]['likes'] not in result_dict:
                result_dict[f'{photos_info[photo]["likes"]}'] = \
                    f'{photos_info[photo]["size"][0]}x{photos_info[photo]["size"][1]}'
                file_name = f'{photos_info[photo]["likes"]}.jpg'
                result_file.append({
                    'file_name': file_name,
                    'size': f'{photos_info[photo]["size"][0]}x{photos_info[photo]["size"][1]}'
                })
            else:
                file_name = f'{photos_info[photo]["likes"]}-{photos_info[photo]["date"]}.jpg'
                result_file.append({
                    'file_name': file_name,
                    'size': f'{photos_info[photo]["size"][0]}x{photos_info[photo]["size"][1]}'
                })
            with open(f'VKCloud/{file_name}', "wb") as file:
                download_url = photos_info[photo]['url']
                picture = requests.get(download_url)
                file.write(picture.content)
        with open(f'VKCloud/info.json', 'w') as file:
            json.dump(result_file, file)





NewUser = VkUser(token)

NewUser.download_photos()








