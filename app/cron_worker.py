import threading
import time
from app.config import config
from app.cleaner import clean_old_results


def start_scheduler(app):
    def loop():
        while True:
            time.sleep(config['CRON_WORK_DELAY'])

            # Создаём контекст приложения, потому что без него функция крутится в отдельном потоке 
            with app.app_context():
                clean_old_results()

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()
    print(f"Крона запущена. Интервал: {config['CRON_WORK_DELAY']} сек.")