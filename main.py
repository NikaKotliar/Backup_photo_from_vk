import requests
from pprint import pprint
import json
from pathlib import Path

with open('vk_token.txt', 'r') as file_object:
    vk_token = file_object.read().strip()
with open('Ya_token.txt', 'r') as file_object:
    Ya_token = file_object.read().strip()
with open('G_drive_token.txt', 'r') as file_object:
    G_drive_token = file_object.readline().strip()


class User:
    def __init__(self, vk_token, Ya_token, G_drive_token):
        self.vk_token = vk_token
        self.Ya_token = Ya_token
        self.G_drive_token = G_drive_token

    def get_users_photos(self, user_id):
        url = 'https://api.vk.com/method/photos.get'

        params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'access_token': self.vk_token,
            'extended': 1,
            'v': '5.131'
        }
        res = (requests.get(url, params)).json()
        with open('photos_list.json', 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=4)

        photos_info = res['response']['items']
        dict_for_upload = {}
        for photo_data in photos_info:
            file_name = str(photo_data['likes']['count']) + '.jpg'
            print(file_name)
            file_link = photo_data['sizes'][-1]
            print (file_link)
            if file_name in dict_for_upload.keys():
                file_name_new = str(photo_data['likes']['count']) + '_' + str(photo_data['date']) + '.jpg'
                dict_for_upload[file_name_new] = file_link['url']
            else:
                dict_for_upload[file_name] = file_link['url']
            print(dict_for_upload)

        with open('photo_list_upload.json', 'w', encoding='utf-8') as f:
            json.dump(dict_for_upload, f, ensure_ascii=False, indent=4)
        return dict_for_upload

    def upload_photo_to_Gdisk (self):
        url = 'https://www.googleapis.com/upload/drive/v3/files'
        headers = {
            "Authorization": 'Bearer {}'.format(self.G_drive_token),
            "Content-type" : 'application/json; charset=UTF-8'
        }
        print(headers)

        para = {
            "name": "test_image.jpg",
        }
        files = {
            'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
            'file': open("./test_image.jpg", "rb")
        }
        r = requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers=headers,
            files=files
        )
        print(r.text)






    # def get_headers(self):
    #     return {
    #         'Content-Type': 'application/json',
    #         'Authorization': 'OAuth {}'.format(self.Ya_token),
    #         'Accept': 'application/json'
    #     }
    #
    # def upload_users_photo(self):
    #     with open("photo_list_upload.json") as f:
    #         data = json.load(f)
    #     for file_name, file_path in data.items():
    #         path_to_disk = str("Backup_photo_from_vk/") + file_name
    #         url_for_load = file_path
    #         url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    #         headers = self.get_headers()
    #         params = {
    #             "url": url_for_load,
    #             "path": path_to_disk,
    #             "disable_redirects": "true"
    #         }
    #         response = requests.post(url, headers=headers, params=params)
    #         response.raise_for_status()
    #         upload_url = (response.json()).get("href", "")
    #         status = requests.get(upload_url, headers=headers)
    #         pprint(status.json())




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
#
#
begemot_korovin = User(vk_token, Ya_token,G_drive_token)
begemot_korovin.upload_photo_to_Gdisk()
# begemot_korovin.get_users_photos(552934290)
# begemot_korovin.upload_users_photo()
