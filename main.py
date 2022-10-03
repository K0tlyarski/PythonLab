import os
import threading
from time import sleep
from tkinter import Image
from PIL import Image, ImageChops
import queue

from bs4 import BeautifulSoup
import requests
import lxml

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


def create_directory(directory_name):
    if not os.path.isdir('dataset'):
        os.mkdir('dataset')
    if not os.path.exists(os.path.join('dataset', directory_name)):
        os.mkdir(os.path.join('dataset', directory_name))


def create_link(request_name):
    for page_number in range(1, 35):
        print(page_number, " page")
        request_name.replace(' ', '%20')
        link = f'https://yandex.ru/images/search?text={request_name}&p={page_number}'
        responce = requests.get(link, headers=header).text
        sleep(2)
        soup = BeautifulSoup(responce, 'lxml')
        image_block = soup.find_all('img', class_='serp-item__thumb justifier__thumb')
        for image in image_block:
            image_link = 'https:' + image.get('src')
            print(image_link)
            yield (image_link)


def download_image(image_link, image_name, folder_name):
    response = requests.get(image_link, headers=header).content

    file_name = open(os.path.join(os.path.join('dataset', folder_name), f"{image_name}.jpg"), 'wb')
    with file_name as handler:
        handler.write(response)


class diff_image(threading.Thread):  # класс по сравнению картинок.
    """Потоковый обработчик"""

    def __init__(self, queue):
        """Инициализация потока"""
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        """Запуск потока"""
        while True:
            # Получаем пару путей из очереди
            files = self.queue.get()
            # Делим и сравниваем
            self.difference_images(files.split(':')[0], files.split(':')[1])
            # Отправляем сигнал о том, что задача завершена
            self.queue.task_done()

    def difference_images(self, img1, img2, path):
        image_1 = Image.open(img1)
        image_2 = Image.open(img2)

        size = [400, 300]  # размер в пикселях
        image_1.thumbnail(size)  # уменьшаем первое изображение
        image_2.thumbnail(size)  # уменьшаем второе изображение

        result = ImageChops.difference(image_1, image_2).getbbox()
        if result is None:
            print(img1, img2, 'matches')
            os.remove(path, img2)
        return


def main_remove(path):
    imgs = os.listdir(path)  # Получаем список картинок
    q = queue.Queue()

    # Запускаем поток и очередь
    for i in range(4):  # 4 - кол-во одновременных потоков
        t = diff_image(q)

        t.start()

        # Даем очереди нужные пары файлов для проверки
    check_file = 0
    current_file = 0

    while check_file < len(imgs):
        if current_file == check_file:
            current_file += 1
            continue
        q.put(path + imgs[current_file] + ':' + path + imgs[check_file])
        current_file += 1
        if current_file == len(imgs):
            check_file += 1
            current_file = check_file

            # Ждем завершения работы очереди
    q.join()


def run(animal_name):
    count = 0
    create_directory(animal_name)
    for url in create_link(animal_name):
        download_image(url, str(count).zfill(4), animal_name)
        count += 1
        sleep(2)
        print(count, ' downloaded')
