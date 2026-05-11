user_settings = {
    "User-Agent" : [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/147.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) Firefox/135.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/147.0.0.0"
    ],
    "Accept-Language" : [
        "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "ru-RU,ru;q=0.9,en;q=0.8",
        "en-US,en;q=0.9,ru;q=0.8",
        "ru,en;q=0.9,en-US;q=0.8"
        ],
    "Accept" : [
        "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        ],
    "Accept-Encoding" : [
        "gzip, deflate, br",
        "gzip, deflate"
        ]
}

search_settings = {
    "1k": {
        "search_url": "https://1k.by/products/search",
        "params": {
            "searchFor": "products",
            "s_categoryid": "0",
            "filter": "retail"
        },
        "keyword_param": "s_keywords"
    },
    "onliner": {
        "search_url": "https://catalog.onliner.by/search",
        "params": {
            # доп. параметров нет
        },  
        "keyword_param": "q"
    }
    # ,
    # "amd":{
    #     "search_url": "",
    #     "params": {
    #         # доп. параметров нет
    #     },  
    #     "keyword_param": "" 
    # }
}