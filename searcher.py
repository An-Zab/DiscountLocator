import requests
import config
import random
import os
import time
import parser
import json

result_folder = "results"
os.makedirs(result_folder, exist_ok=True)


def get_headers():
    """Формирует случайную комбинацию хэдеров для запроса"""
    headers = {}
    for key, value in config.user_settings.items():
        headers[key] = random.choice(value)
    return headers


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
        response = requests.get(url, params=params)
        print(f"Получил {response.url}, статус: {response.status_code}")
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
            response = requests.get(url, params=params)
            print(f"Получил {response.url}, статус: {response.status_code}")
            
            with open(f"{result_folder}/{filename}_{page_num}_response.html", "w", encoding="utf-8") as file:
                file.write(response.text)
            offer_list.extend(parser.receive_offer_place(response.text))

        with open(f"{result_folder}/offer_list.json", "w", encoding="utf-8") as file:
            json.dump(offer_list, file, indent=2, ensure_ascii=False)

    #Добавил срез списка для тестов
    for offer_url in offer_list[:3]:
        if '1k.by' in offer_url:
            time.sleep(random.uniform(1, 2))
            response = requests.get(offer_url)
            shops = parser.receive_contact_info(response.text)
            all_contacts.extend(shops)

    with open(f"{result_folder}/contacts.json", "w", encoding="utf-8") as file:
        json.dump(all_contacts, file, indent=2, ensure_ascii=False)

    return offer_list, all_contacts
test_result = search_product("iphone 11")
print(test_result)