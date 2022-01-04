import requests
import json
from datetime import datetime
from pprint import pprint
import os


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token='958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
                 version='5.131'):
        self.params = {
            'access_token': token,
            'v': version
        }

    def get_photos_allinfo(self, owner_id: str):
        get_photos_url = self.url + 'photos.get'
        get_photos_params = {
            'owner_id': owner_id,
            'album_id': 'profile',
            'extended': '1'
        }
        res = requests.get(get_photos_url, params={**self.params, **get_photos_params}).json()
        return res

    def sort_photos_info(self, owner_id: str):
        photos_info = {}
        res = self.get_photos_allinfo(owner_id)
        for item in res['response']['items']:
            photos_info[item['id']] = {}
            photos_info[item['id']]['likes'] = item['likes']['count']
            photos_info[item['id']]['date'] = \
                datetime.utcfromtimestamp(int(item['date'])).strftime('%Y-%m-%d %H:%M:%S')
            photos_info[item['id']]['size'] = [item['sizes'][-1]['height'], item['sizes'][-1]['width']]
            photos_info[item['id']]['url'] = item['sizes'][-1]['url']
        return photos_info

    def download_photos(self, owner_id: str):
        result_dict = {}
        result_file = []
        photos_info = self.sort_photos_info(owner_id)
        os.makedirs('VKCloud', exist_ok = True)
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
        pprint(result_file)
        return result_file


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {'Content-Type': 'application/json',
                'Authorization': f'OAuth {self.token}'}

    def put_new_folder(self, folder_name):
        new_folder_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': folder_name}
        response = requests.put(new_folder_url, headers=headers, params=params)
        return response.json

    def get_upload_link(self, file):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": f"VKCloud/{file}", "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload(self, file_path: str):
        file = file_path.split('/')[-1]
        href = self.get_upload_link(file=file).get("href", "")
        response = requests.put(href, data=open(file_path, 'rb'))
        response.raise_for_status()

    def multiple_upload(self, files):
        self.put_new_folder('VKCloud')
        for file in files:
            self.upload(f'VKCloud/{file["file_name"]}')



if __name__ == '__main__':
    token = input('Введите ваш Token: ')
    owner_id = str(input('Введите ID пользователя: '))
    NewUser = VkUser()
    files_list = NewUser.download_photos(owner_id)
    uploader = YaUploader(token)
    uploader.multiple_upload(files_list)















