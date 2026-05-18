import requests
import config
import random
import os
import time
import parser
import json
from bs4 import BeautifulSoup
from utils import get_headers

result_folder = "results"
os.makedirs(result_folder, exist_ok=True)


def search_product(product):
    offer_list = []
    url_list = []
    all_contacts = []

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

    for url, params in urls:
        time.sleep(random.uniform(1,3))
        response = requests.get(url, params=params, headers=get_headers())
        print(f"Получил {response.url}, статус: {response.status_code}")

    
        if 'onliner.by' in url:
            products = parser.parse_onliner_search(response.text)
            print(f"Найдено товаров: {len(products)}")
            for prod in products:
                time.sleep(random.uniform(1, 2))
                shops = parser.receive_contact_info_from_onliner(prod['api_url'], prod['name'])
                all_contacts.extend(shops)
            continue


        filename = url.split("//")[1].split("/")[0]
        #Сплитим URL, чтобы сделать понятное название сохраняемого файла
        total_pages = parser.get_page_max_num(response.text)
        
        with open(f"{result_folder}/{filename}_1_response.html", "w", encoding="utf-8") as file:
                file.write(response.text)

        offer_list.extend(parser.receive_offer_place(response.text))
        for page_num in range(2, total_pages + 1):
            params = params.copy()
            params['page'] = page_num
            time.sleep(random.uniform(1,3))
            response = requests.get(url, params=params, headers=get_headers())
            print(f"Получил {response.url}, статус: {response.status_code}")
            
            with open(f"{result_folder}/{filename}_{page_num}_response.html", "w", encoding="utf-8") as file:
                file.write(response.text)
            offer_list.extend(parser.receive_offer_place(response.text))

        with open(f"{result_folder}/offer_list.json", "w", encoding="utf-8") as file:
            json.dump(offer_list, file, indent=2, ensure_ascii=False)

    # Добавил срез списка для тестов
    for offer_url in offer_list[:7]:
        if '1k.by' in offer_url:
            time.sleep(random.uniform(1, 2))
            response = requests.get(offer_url,headers=get_headers())
            shops = parser.receive_contact_info_from_1k(response.text)
            all_contacts.extend(shops)

    with open(f"{result_folder}/contacts.json", "w", encoding="utf-8") as file:
        json.dump(all_contacts, file, indent=2, ensure_ascii=False)

    return offer_list, all_contacts
test_result = search_product("macbook Air 15 M4 16/256")
print(test_result)