import requests
import os
from tqdm import tqdm
from time import sleep
from pprint import pprint
import datetime
import json
import random
import string

info_file = []
chars = string.ascii_letters + string.punctuation

def random_string_generator(str_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(str_size))


class VK_Uploader:
    def __init__(self, id_vk: str, ya_token: str, album='profile', quan=5):
        self.album = album
        self.id_vk = id_vk
        self.ya_token = ya_token
        self.quan = quan

    def get_photos(self):
        with open('D:\\Vikas_documents\\python\\requests_vk\\token_vk.txt','r') as token_file:
            token = token_file.readline()
            r = requests.get( "https://api.vk.com/method/photos.get?id="+id_vk+"&album_id="+self.album+"&extended=1&count=1000&access_token="+token.strip()+"&v=5.131&")
            res = r.json()
        url = "https://cloud-api.yandex.net/v1/disk/resources?path=%2Fphoto_" + self.album + '_' + datetime.datetime.today().strftime("%Y%m%d_%H-%M")
        headers = {'Accept': 'application/json', "Authorization": 'OAuth ' + ya_token}
        requests.put(url, headers=headers)
        likes_list = []
        if self.quan > len(res['response']['items']) and self.quan != 5 :
            print ('количество запрошенных фотографий превышает имеющиеся')
            return
        elif self.quan > 1000 :
            print('количество запрошенных фотографий превышает установленные vk лимиты')
            return
        elif self.quan == 5 and len(res['response']['items']) < 5 :
            self.quan = len(res['response']['items'])
            pass
        else:
            pass
        try :
            for i in tqdm(range(self.quan)) :
                url_upl = "https://cloud-api.yandex.net/v1/disk/resources/upload"
                likes = str(res['response']['items'][i]['likes']['count'])
                if likes not in likes_list:
                    likes_list.append(likes)
                else:
                    likes = likes + '_' + random_string_generator(2, chars)
                params1 = {'path': '/photo_'+ self.album + '_' + datetime.datetime.today().strftime("%Y%m%d_%H-%M")+ '/' + likes, 'overwrite': False}
                r1 = requests.get(url_upl, params1, headers=headers)
                res1 = r1.json()
                pic = requests.get(res['response']['items'][i]['sizes'][-1]['url'])
                upload = requests.put(url=res1['href'], data=pic.content)
                info = {"file_name": likes,"size": res['response']['items'][i]['sizes'][-1]['type']}
                info_file.append(info)
                sleep(.01)
            print('файлы загружены в папку photo_',self.album,'_',datetime.datetime.today().strftime("%Y%m%d_%H"),'**',sep='')
        except KeyError:
            print('что то пошло не так, возможно на диске нет места, проверьте и попробуйте еще раз')
        return


if __name__ == '__main__':
    print('для загрузки фотографий с профиля на Yandex диск пожалуйста предоставьте необходимые данные')
    id_vk = input('введите Id пользователя в VK ')
    ya_token = input('введите token пользователя для yandex disk ')
    quant = input('введите количество фотографий, по умолчанию будут сохранены имеющиеся, но не более 5 ')
    if quant != '' :
        quan = int(quant)
        vk_uploader = VK_Uploader(id_vk, ya_token, album='profile', quan = quan)
        vk_uploader.get_photos()
    else:
        vk_uploader = VK_Uploader(id_vk, ya_token)
        vk_uploader.get_photos()

    answ = input('Вы желаете просмотреть информационный файл (Y) или сохранить на компьютере (N)? ')
    if str.upper(answ) == 'Y' :
         pprint(info_file)
    else :
         path_save = input('введите путь к папке, например - c://temp ')
         with open(path_save+'/info_file_'+datetime.datetime.today().strftime("%Y%m%d_%H-%M")+'.json', 'w') as f:
             json.dump(info_file, f, ensure_ascii=False, indent=2)
         print('информационный файл загружен')

    answ2 = input('желаете загрузить на Yandex диск фото со стены? ')
    if str.upper(answ2) == 'Y' :
        quant1 = input('введите количество фотографий, по умолчанию будут сохранены имеющиеся, но не более 5  ')
        if quant1 != '' :
            quan1 = int(quant1)
            vk_uploader = VK_Uploader(id_vk, ya_token, 'wall', quan=quan1)
            vk_uploader.get_photos()
        else:
            vk_uploader = VK_Uploader(id_vk, ya_token, 'wall')
            vk_uploader.get_photos()
    else :
         print('работа программы завершена')




