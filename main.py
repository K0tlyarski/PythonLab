from bs4 import BeautifulSoup
import requests
import lxml
import os
from time import sleep

header = {
'Connection': 'keep-alive',
'Cache-Control': 'max-age=0',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 '
'Safari/537.36 OPR/40.0.2308.81',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'DNT': '1',
'Accept-Encoding': 'gzip, deflate, lzma, sdch',
'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
}
def create_directory(dir_name):
    if not os.path.isdir('dataset'):
        os.mkdir('dataset')
    if not os.path.exists(f'dataset/{dir_name}'):
        os.mkdir(f'dataset/{dir_name}')

def create_link(request_name):
    for page_number in range(1, 3):
        print(page_number, " page")
        request_name.replace(' ', '%20')
        link = f'https://yandex.ru/images/search?text={request_name}&p={page_number}'
        responce = requests.get(link, headers = header).text

        sleep(2)
        soup = BeautifulSoup(responce, 'lxml')
        image_block = soup.find_all('img', class_='serp-item__thumb justifier__thumb')
        for image in image_block:
            image_link = 'https:' + image.get('src')
            print(image_link)
            yield (image_link)

def download_image(image_link, image_name, folder_name):
    response = requests.get(image_link).content
    file = open(f"dataset/{folder_name}/{image_name}.jpg", "wb")
    with open(f"dataset/{folder_name}/{image_name}.jpg", "wb") as handler:
        handler.write(response)

