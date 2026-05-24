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
    return render_template('results.html', query=query, results=results, contacts=all_contacts, searched_at=history.searched_at)