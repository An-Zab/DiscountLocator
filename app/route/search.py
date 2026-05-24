from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.search_history import SearchHistory
from app.models.search_result import SearchResult
from app.searcher import search_product

bp = Blueprint('search', __name__)


@bp.route('/search')
@login_required
def search():
    query = request.args.get('q', '').strip()
    if not query:
        flash('Введите запрос', 'error')
        return redirect(url_for('index'))

    # Запускаем парсер
    offer_list, all_contacts = search_product(query)

    # Сохраняем в историю поиска
    history = SearchHistory(
        user_id=current_user.id,
        query=query
    )
    db.session.add(history)
    db.session.flush()  # чтобы получить history.id до коммита

    # Сохраняем результаты
    for contact in all_contacts:
        if 'message' in contact:
            continue  # пропускаем "ничего не найдено"
        result = SearchResult(
            search_id=history.id,
            product=contact.get('product', ''),
            shop_name=contact.get('shop_name', ''),
            product_price=contact.get('product_price', ''),
            shop_phones=', '.join(contact.get('shop_phones', [])),
            shop_social_media=', '.join(contact.get('shop_social_media', [])),
            placement=contact.get('placement', ''),
            url=contact.get('url', ''),
            offertimestamp=contact.get('offertimestamp', 0)
        )
        db.session.add(result)

    db.session.commit()

    results = SearchResult.query.filter_by(search_id=history.id).all()



    price_list = []
    for item in results:
        try:
            price_str = item.product_price.replace('б.р.', '').replace(' ', '').replace(',', '.').strip()
            price_list.append((float(price_str), item.id))
        except:
            pass

    price_list.sort(key=lambda x: x[0])
    top_offers = []
    for item in price_list[:10]:   
        top_offers.append(item[1])
    bad_offers = [item[1] for item in price_list[-3:]]

    if price_list:
        medium_price = round(sum(p[0] for p in price_list) / len(price_list), 2)
    else:
        medium_price = 0

    return render_template('results.html', query=query, results=results, contacts=all_contacts, searched_at=history.searched_at, top_offers=top_offers, bad_offers=bad_offers, medium_price=medium_price)