import random
import config
import time
import requests
from typing import Callable

def get_headers():
    """Формирует случайную комбинацию хэдеров для запроса"""
    headers = {}
    for key, value in config.user_settings.items():
        headers[key] = random.choice(value)
    return headers


def retry_on_error(retry = 4, delay = 3):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            delay_in_wrapper = delay
            tries = 1
            for tries in range(1, retry + 1):
                try:
                    return func(*args, **kwargs)
                except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                    print(f"Установить соединение не удалось: {e}.\nКоличество попыток: {tries}")
                    if tries <= retry:
                        print(f'Текущий дилэй = {delay_in_wrapper}')
                        time.sleep(delay_in_wrapper)
                        delay_in_wrapper = delay_in_wrapper+random.randint(1,delay_in_wrapper)
                        
            return None
        return wrapper
    return decorator

@retry_on_error()
def improved_request(url, *args, **kwargs):
    return requests.get(url, *args, **kwargs)