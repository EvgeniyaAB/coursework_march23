from pprint import pprint
import requests
import time
from tqdm import tqdm

class VKontakte:
    def __init__(self, token, id):
        self.vk_url = 'https://api.vk.com/method/'

        self.params = {
            'v': '5.131',
            'access_token': token,
            'owner_id': id
        }
    def get_photos(self, count=5, offset=0):
        photos_vk_url = self.vk_url + 'photos.get'
        photos_params = {
            'album_id': 'profile',
            'extended': True,
            'photo_sizes': True,
            'offset': offset,
            'count': count
        }
        try:
            response = requests.get(url=photos_vk_url, params={**self.params, **photos_params})
            reg = response.json()
            all_photos = reg['response']['items']
        except:
            print('!! Error')

        photos_json =[]
        temporary_list = []
        for photo_size in all_photos:
            photo_url = photo_size['sizes'][-1]['url']
            if photo_size['likes']['count'] not in temporary_list:
                photo_name = f"{photo_size['likes']['count']}.jpeg"
                temporary_list.append(photo_size['likes']['count'])
            else:
                photo_name = f"{photo_size['likes']['count']}{photo_size['date']}.jpeg"
                temporary_list.append(photo_name)
            photos_json.append(
            {"file_name": photo_name,
            "size": photo_size['sizes'][-1]['type'],
             "url": photo_url})
            time.sleep(0.1)


        return photos_json

class YandexDisk:
    def __init__(self, token):
        self.yandex_url = 'https://cloud-api.yandex.net/'
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': self.token
        }
    def create_folder(self, folder_name):
        folder_url = f'{self.yandex_url}v1/disk/resources'
        params = {"path": folder_name, "overwrite": "true"}
        headers = self.get_headers()
        try:
            folder = requests.put(url=folder_url, headers=headers, params=params)

            if folder.status_code == 201:
                print(f"Папка {folder_name} успешно создана")
            elif folder.status_code == 409:
                print(f"Папка {folder_name} уже существует")
            return folder_name
        except:
            print('!! Error create')

    def get_upload_link(self, folder_name):
        photos_json = vk.get_photos()
        for json in photos_json:
            photo_url = json['url']
            disk_file_path = f"{folder_name}/{json['file_name']}"
            upload_url = f'{self.yandex_url}v1/disk/resources/upload'
            headers = self.get_headers()
            params = {"path": disk_file_path, "url": photo_url}
            try:
                response = requests.post(url=upload_url, headers=headers, params=params)
                for i in tqdm(response.json()):
                    time.sleep(0.2)
                if response.status_code == 202:
                    print("Загружено успешно")
            except:
                print('!! Error download')



if __name__ == '__main__':
    vk = VKontakte(token='TOKEN', id='ID')
    pprint(vk.get_photos())
    ya = YandexDisk(token='TOKEN')
    ya.get_upload_link(ya.create_folder(folder_name=input('Введи название папки: ')))
