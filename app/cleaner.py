import time
from app.config import config
from app.extensions import db
from app.models.search_result import SearchResult


def clean_old_results():
    now = int(time.time())
    current_delay = now - config['CLEAN_DELAY']
    old_results = SearchResult.query.filter(SearchResult.offertimestamp < current_delay).all()
    count = len(old_results)
    for item in old_results:
        db.session.delete(item)
    db.session.commit()
    if count:
        print(f"Cleaner очистил {count} старых результатов")
    return count