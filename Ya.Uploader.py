import requests
from pprint import pprint


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


if __name__ == '__main__':
    path_to_file = input('Введите путь к файлу: ')
    token = input('Введите ваш Token: ')
    uploader = YaUploader(token)
    # result = uploader.put_new_folder('VKCloud')
    result = uploader.upload(path_to_file)