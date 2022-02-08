import requests
import time
import main

with open('Ya_token.txt', 'r') as file_object:
    Ya_token = file_object.read().strip()


def test_create_file_for_photo():
    folder_name = 'Backup_from_vk_test' + str(time.time() * 1000.0)
    user = main.User('doesnt_matter', Ya_token)
    respond = user.create_file_for_photo(folder_name)
    assert respond.__str__() == '<Response [201]>'

    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    params = {
        "path": 'disk:/' + folder_name,
        "fields": 'name,_embedded.items.path'
    }
    folder_info = requests.get(
        url, params,
        headers=user.get_headers(),
    )
    assert folder_info.status_code == 200


def test_error_on_duplicate():
    user = main.User('doesnt_matter', Ya_token)
    folder_name = 'Backup_from_vk_test' + str(time.time() * 1000.0)
    respond = user.create_file_for_photo(folder_name)
    assert respond.__str__() == '<Response [201]>'
    respond = user.create_file_for_photo(folder_name)
    assert respond.__str__() == '<Response [409]>'
