import random
import config


def get_headers():
    """Формирует случайную комбинацию хэдеров для запроса"""
    headers = {}
    for key, value in config.user_settings.items():
        headers[key] = random.choice(value)
    return headers
