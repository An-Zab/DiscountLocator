from bs4 import BeautifulSoup



def get_page_max_num(htmlpage):
    """Определяет число страниц-результатов поиска по классу paging__it"""
    soup = BeautifulSoup(htmlpage, 'lxml')
    last_page = soup.find_all(class_="paging__it")
    if last_page:
        return int(last_page[-1].get_text())
    else:
        return 1

