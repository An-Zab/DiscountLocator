from bs4 import BeautifulSoup
import re
import json
import requests
from utils import get_headers

def get_page_max_num(htmlpage):
    """Определяет число страниц-результатов поиска по классу paging__it"""
    soup = BeautifulSoup(htmlpage, 'lxml')
    last_page = soup.find_all(class_="paging__it")
    if last_page:
        return int(last_page[-1].get_text())
    else:
        return 1

def receive_offer_place(htmlpage):
    soup = BeautifulSoup(htmlpage, 'lxml')
    links = []
    for link in soup.find_all(class_={"prod__ext", "button-style button-style_secondary button-style_small-alter catalog-form__button catalog-form__button_min-width_xxxss"}):
        href = link.get('href')
        if href and ('/offers/' in href or '/prices' in href):
            links.append(href) 
    return links

def receive_contact_info_from_1k(htmlpage):
    contact_info = []
    soup = BeautifulSoup(htmlpage, 'lxml')

    for seller in soup.find_all('section', class_='seller'):
        shop = {}
        
        product_tag = soup.find_all('a', class_='crumbs__it')
        product_name = product_tag[-1].text.strip() if product_tag else 'Неизвестный товар'
        shop['product'] = product_name

        logo = seller.find('img', class_='seller__logo')
        shop['shop_name'] = logo['alt'].strip() 
        
        price_tag = seller.find(class_='seller__price')
        shop['product_price'] = price_tag.text.strip() if price_tag else 'Нет цены'

        contacts = seller.find(attrs={"data-communicationinfourl": True})
        if contacts:
            api_link = contacts.get('data-communicationinfourl') 
            full_url = "https://1k.by" + api_link
            response = requests.get(full_url, headers=get_headers())
            shop['shop_phones'] = list(set(re.findall(r'tel:(\+\d+)', response.text)))
            shop['shop_social_media'] = list(set(re.findall(r'[\w.]+@[\w.]+', response.text)))
        else:
            shop['phones'] = []
            shop['social_media'] = []
        
        shop_link = seller.find('a', class_='seller__link')
        shop['url'] = shop_link['href'] if shop_link else None

        contact_info.append(shop)

    return contact_info

def parse_onliner_search(htmlpage):
    soup = BeautifulSoup(htmlpage, 'lxml')

    # Названия товаров из тегов <h3>
    names = []
    for h3 in soup.find_all('h3'):
        text = h3.text.strip()
        if text:
            names.append(text)

    # СОБИРАЕМ API-ССЫЛКИ (для получения магазинов/цен)
    # Ищем URL типа: https://shop.api.onliner.by/products/.../positions
    api_urls = re.findall(
        r'https:\\u002F\\u002Fshop\.api\.onliner\.by\\u002Fproducts\\u002F[^"]+?positions',
        htmlpage
    )

    # СОБИРАЕМ ССЫЛКИ НА СТРАНИЦУ ТОВАРА (placement)
    # Ищем URL типа: https://catalog.onliner.by/.../.../prices
    placement_urls = re.findall(
        r'https:\\u002F\\u002Fcatalog\.onliner\.by\\u002F[^"]+?\\u002Fprices',
        htmlpage
    )


    # СОБИРАЕМ ВСЁ ВМЕСТЕ
    products = []
    for name, api_url, placement in zip(names, api_urls, placement_urls):
        # Заменяем \u002F на обычный слэш /
        clean_api_url = api_url.replace('\\u002F', '/')
        clean_placement = placement.replace('\\u002F', '/')


        products.append({
            'name': name,           # Название товара
            'api_url': clean_api_url,  # API для получения магазинов
            'html_url': clean_placement  # Ссылка на страницу товара (placement)
        })

    return products

def receive_contact_info_from_onliner(product_url, product_name='', placement=''):
    server_response = requests.get(product_url)
    data = server_response.json()
    shops = data.get('shops', {})
    positions = data.get('positions', {}).get('primary', [])
    
    contact_info = []
    for pos in positions:
        shop_id = str(pos['shop_id'])
        shop = shops.get(shop_id, {})
        
        clean_product_url = placement
        shop_data = {
            'product': product_name,
            'shop_name': shop.get('title', 'Неизвестный'),
            'product_price': pos['position_price']['amount'] + ' б.р.',
            'placement': clean_product_url,
            'url': shop.get('html_url', ''),
            'shop_phones': shop.get('schema_phones', []),
            'shop_social_media': [],
        }
        contact_info.append(shop_data)
        
    return contact_info


# test_html = '''"url":"https:\\u002F\\u002Fshop.api.onliner.by\\u002Fproducts\\u002Fiphone1164b\\u002Fpositions"'''
# test_html = '<h3>Телефон Apple iPhone 11 64GB (черный)</h3>' + test_html

# print(parse_onliner_search(test_html))

