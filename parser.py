from bs4 import BeautifulSoup
import requests
import lxml
import config
import random

def get_headers():
    """Формирует случайную комбинацию хэдеров для запроса"""
    headers = {}
    for key, value in config.user_settings.items():
        headers[key] = random.choice(value)
    return headers


def search_product(product):
    url_list = []
    def create_url(product):
        """Формирует список кортежей (search_url, {params и изменённый keyword_param}) 
        для requests.get()"""
        for key, value in config.search_settings.items():
            params = value['params'].copy() 
            params[value['keyword_param']] = product 
            #Сделали копию params из search_settings и добавили в него строку keyword_param : product 
            url_list.append((value['search_url'], params)) 
        return url_list
    
    urls = create_url(product)
    responses = []

    for url, params in urls:
        response = requests.get(url, params=params)
        responses.append(response)
        print(f"Получил {response.url}, статус: {response.status_code}")
    return responses
result = search_product("iphone 11")

