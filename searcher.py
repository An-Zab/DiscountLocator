import requests
import config
import random
import os
import time
import parser
import json
from bs4 import BeautifulSoup
from utils import get_headers
from utils import improved_request

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
        if 'onliner.by' in url:
            response = improved_request(url, params=params)  # без headers, т.к. онлайнер периодически ругается на хэдеры и не отдаёт инфу
        else:
            response = improved_request(url, params=params, headers=get_headers())
        if response is None:
            print(f"Пропускаем из-за ошибки сети. Проблема возникла в {create_url.__name__} на этапе отправки поискового запроса")
            continue
        print(f"Получил {response.url}, статус: {response.status_code}")

    
        if 'onliner.by' in url:
            products = parser.parse_onliner_search(response.text)
            print(f"Найдено товаров: {len(products)}")
            for prod in products:
                time.sleep(random.uniform(1, 2))
                shops = parser.receive_contact_info_from_onliner(
                    prod['api_url'],
                    prod['name'],
                    prod['html_url']
                )
                all_contacts.extend(shops)
            continue

        #Сплитим URL, чтобы сделать понятное название сохраняемого файла
        filename = url.split("//")[1].split("/")[0]
        

        #Обрезал колиечество страниц для теста
        total_pages = min(parser.get_page_max_num(response.text), 2)
        
        # with open(f"{result_folder}/{filename}_1_response.html", "w", encoding="utf-8") as file:
        #         file.write(response.text)

        offer_list.extend(parser.receive_offer_place(response.text))
        for page_num in range(2, total_pages + 1):
            params = params.copy()
            params['page'] = page_num
            time.sleep(random.uniform(1,3))
            response = improved_request(url, params=params, headers=get_headers())
            if response is None:
                print(f"""Пропускаем из-за ошибки сети. Проблема возникла в {create_url.__name__} на этапе получения ответов с разных страниц. 
                      Страница {page_num} урла {url}""")
                continue
            print(f"Получил {response.url}, статус: {response.status_code}")
            
        #     with open(f"{result_folder}/{filename}_{page_num}_response.html", "w", encoding="utf-8") as file:
        #         file.write(response.text)
        #     offer_list.extend(parser.receive_offer_place(response.text))

        # with open(f"{result_folder}/offer_list.json", "w", encoding="utf-8") as file:
        #     json.dump(offer_list, file, indent=2, ensure_ascii=False)

    #Обрезал колиечество офферов со страницы для теста
    for offer_url in offer_list[:2]:
        if '1k.by' in offer_url:
            time.sleep(random.uniform(1, 2))
            response = improved_request(offer_url,headers=get_headers())
            shops = parser.receive_contact_info_from_1k(response.text, placement=offer_url)
            all_contacts.extend(shops)
    
    if not all_contacts:
        all_contacts.append({
            "message": f"По запросу - «{product}» - ничего не найдено",
            "offertimestamp": int(time.time())
        })

    with open(f"{result_folder}/contacts.json", "w", encoding="utf-8") as file:
        json.dump(all_contacts, file, indent=2, ensure_ascii=False)

    return offer_list, all_contacts
test_result = search_product("iphone 17")
# print(test_result)