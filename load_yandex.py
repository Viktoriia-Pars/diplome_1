import requests
import os
files = input('введите список файлов для загрузки через запятую, пример ввода: d://Documents/test.txt ')
file_list = files.split(',')
class YaUploader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def upload(self):
        with open('D:\\Vikas_documents\\python\\token_yandex_disc.txt','r') as token_file:
            token = token_file.readline()
            headers = {'Accept': 'application/json', "Authorization": 'OAuth ' + token.strip()}
            path_name = (self.file_path).split('/')[-1]
            params = {'path': 'Test/'+ path_name, 'overwrite': False}

            url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
            r = requests.get(url, params, headers=headers)
            res = r.json()
            try:
                upload = requests.put(url=res['href'], data=open(self.file_path, 'rb'))
                if upload.status_code == 201:
                    print('файл успешно загружен')
            except KeyError:
                print('файл с таким именем уже есть, выберете для загрузки другой файл')
            return

if __name__ == '__main__':
    for i in range(len(file_list)) :
        uploader = YaUploader(file_list[i])
        result = uploader.upload()