from bs4 import BeautifulSoup
import re
import json
import requests

def get_page_max_num(htmlpage):
    """Определяет число страниц-результатов поиска по классу paging__it"""
    soup = BeautifulSoup(htmlpage, 'lxml')
    last_page = soup.find_all(class_="paging__it")
    if last_page:
        return int(last_page[-1].get_text())
    else:
        return 1


# with open('results/catalog.onliner.by_1_response.html', 'r', encoding='UTF-8') as file:
#     html_page_content = file.read()	

def receive_offer_place(htmlpage):
    soup = BeautifulSoup(htmlpage, 'lxml')
    links = []
    for link in soup.find_all(class_={"prod__ext", "button-style button-style_secondary button-style_small-alter catalog-form__button catalog-form__button_min-width_xxxss"}):
        href = link.get('href')
        if href and ('/offers/' in href or '/prices' in href):
            links.append(href) 
    return links

# print(receive_offer_place(html_page_content))


def receive_contact_info(htmlpage):
    contact_info = []
    soup = BeautifulSoup(htmlpage, 'lxml')

    for seller in soup.find_all('section', class_='seller'):
        shop = {}
        
        # Находит название продавца
        logo = seller.find('img', class_='seller__logo')
        shop['name'] = logo['alt'].strip() 
        
        
        # Находит цену товара
        price_tag = seller.find(class_='seller__price')
        shop['price'] = price_tag.text.strip() if price_tag else 'Нет цены'

        # Находит контакты через API
        contacts = seller.find(attrs={"data-communicationinfourl": True})
        if contacts:
            api_link = contacts.get('data-communicationinfourl') 
            full_url = "https://1k.by" + api_link
            response = requests.get(full_url)
            shop['phones'] = list(set(re.findall(r'tel:(\+\d+)', response.text)))
            shop['social_media'] = list(set(re.findall(r'[\w.]+@[\w.]+', response.text)))
        else:
            shop['phones'] = []
            shop['social_media'] = []
        
        # Находит карточку продавца
        shop_link = seller.find('a', class_='seller__link')
        shop['url'] = shop_link['href'] if shop_link else None

        contact_info.append(shop)

    return contact_info


