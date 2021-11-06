import requests
from pprint import pprint
import json
from pathlib import Path

with open('vk_token.txt', 'r') as file_object:
    vk_token = file_object.read().strip()
with open('Ya_token.txt', 'r') as file_object:
    Ya_token = file_object.read().strip()


class User:
    def __init__(self, vk_token, Ya_token):
        self.vk_token = vk_token
        self.Ya_token = Ya_token

    with open('vk_token.txt', 'r') as file_object:
        vk_token = file_object.read().strip()

    def get_users_photos(self, user_id):
        url = 'https://api.vk.com/method/photos.get'

        params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'access_token': vk_token,
            'extended': 1,
            'v': '5.131'
        }
        res = (requests.get(url, params)).json()
        photos_info = res['response']['items']
        dict_for_upload = {}
        for photo_data in photos_info:
            file_name = str(photo_data['likes']['count']) + '.jpg'
            file_link = photo_data['sizes'][-1]
            if file_name in dict_for_upload.keys():
                file_name_new = file_name + '_' + str(photo_data['date'])
                dict_for_upload[file_name_new] = dict_for_upload.pop(file_name)
            else:
                dict_for_upload[file_name] = file_link
        with open('photo_list_upload.json', 'w', encoding='utf-8') as f:
            json.dump(dict_for_upload, f, ensure_ascii=False, indent=4)
        return dict_for_upload

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.Ya_token),
            'Accept': 'application/json'
        }

    def upload_users_photo(self):
        with open("photo_list_upload.json") as f:
            data = json.load(f)
        for file_name, file_path in data.items():
            path_to_disk = Path("Backup_photo_from_vk/", file_name)
            url_for_load = file_path['url']
            url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            headers = self.get_headers()
            params = {
                "url": url_for_load,
                "path": path_to_disk,
                "disable_redirects": "true"
            }
            response = requests.post(url, headers=headers, params=params)
            response.raise_for_status()
            upload_url = (response.json()).get("href", "")
            status = requests.get(upload_url, headers=headers)
            pprint(status.json())

            return status.json()

    #         if response.status_code == 202:
    #         print("Загрузка успешна")
    #         # pprint(response.json())
    #         return response.json()
    #
    # # def get_load_info(self):
    # #     upload_url = self.upload_users_photo().get("href", "")
    # #     headers = self.get_headers()
    # #     status = requests.get(upload_url, headers=headers)
    # #     pprint(status.json())
    # #     return status.json()

begemot_korovin = User(vk_token, Ya_token)
begemot_korovin.get_users_photos(552934290)
begemot_korovin.upload_users_photo()
