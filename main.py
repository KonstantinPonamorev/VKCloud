import requests
import time
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

    def get_photos(self):
        get_photos_url = self.url + 'photos.get'
        get_photos_params = {
            'album_id': 'profile',
            'extended': '1'
        }
        res = requests.get(get_photos_url, params={**self.params, **get_photos_params}).json()
        pprint(res)


NewUser = VkUser(token)
NewUser.get_photos()





