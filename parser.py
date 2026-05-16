from bs4 import BeautifulSoup



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

# 1k.by_2_response.html
# catalog.onliner.by_1_response.html
def receive_offer_place(htmlpage):
    soup = BeautifulSoup(htmlpage, 'lxml')
    links = []
    for link in soup.find_all(class_={"prod__ext", "button-style button-style_secondary button-style_small-alter catalog-form__button catalog-form__button_min-width_xxxss"}):
        href = link.get('href')
        if href and ('/offers/' in href or '/prices' in href):
            links.append(href)
        # links.append(link.get('href'))  
    return links

# print(receive_offer_place(html_page_content))

