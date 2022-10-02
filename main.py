from bs4 import BeautifulSoup
import requests
import lxml
import os
from time import sleep

def create_directory(dir_name):
    if not os.path.isdir('dataset'):
        os.mkdir('dataset')
    if not os.path.exists(f'dataset/{dir_name}'):
        os.mkdir(f'dataset/{dir_name}')
