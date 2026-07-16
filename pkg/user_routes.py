from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
from pkg.models import (db, TbArtist, TbPatron, TbArt, TbArtType,
                         RatingReview, MessageChat, UserSearchTrack,
                         OrderPurchase, OrderPurchaseDetail)
from datetime import datetime

user = Blueprint('user', __name__)


def login_required(user_type=None):
    """Helper to check session."""
    if 'user_id' not in session:
        return False
    if user_type and session.get('user_type') != user_type:
        return False
    return True


# ─────────────────────────────────────────
# ARTIST PAGES
# ─────────────────────────────────────────
@user.route('/artist/dashboard')
def artist_dashboard():
    if not login_required('artist'):
        return redirect(url_for('auth.login'))
    artist = db.session.query(TbArtist).get(session['user_id'])
    arts   = db.session.query(TbArt).filter(TbArt.artist_art_id == session['user_id']).all()
    orders = db.session.query(OrderPurchase).filter(
        OrderPurchase.artist_ord_id == session['user_id']
    ).order_by(OrderPurchase.order_date.desc()).limit(5).all()
    return render_template('artist/artist_dashboard.html',
                           artist=artist, arts=arts, orders=orders)


@user.route('/artist/profile')
def artist_profile():
    if not login_required('artist'):
        return redirect(url_for('auth.login'))
    artist = db.session.query(TbArtist).get(session['user_id'])
    return render_template('artist/artist_page(public_facing).html', artist=artist)


@user.route('/artist/upload', methods=['GET'])
def upload_art():
    if not login_required('artist'):
        return redirect(url_for('auth.login'))
    art_types = db.session.query(TbArtType).all()
    return render_template('art/upload_art_page.html', art_types=art_types)


@user.route('/artist/upload', methods=['POST'])
def upload_art_post():
    if not login_required('artist'):
        return jsonify({'status': 'error', 'message': 'Not logged in.'})

    title      = request.form.get('title', '').strip()
    desc       = request.form.get('description', '').strip()
    price      = request.form.get('price', 0)
    image      = request.form.get('image', '').strip()
    art_type   = request.form.get('art_type_id')
    stock      = request.form.get('stock_qty', 1)

    if not all([title, price, image]):
        return jsonify({'status': 'error', 'message': 'Title, price and image are required.'})

    new_art = TbArt(
        art_title=title,
        art_desc=desc,
        art_price=float(price),
        art_image=image,
        art_type_id=int(art_type) if art_type else None,
        artist_art_id=session['user_id'],
        stock_qty=int(stock),
        artwork_status='available',
        art_date=datetime.utcnow()
    )
    db.session.add(new_art)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Artwork uploaded successfully!'})


@user.route('/artist/artworks')
def my_artworks():
    if not login_required('artist'):
        return redirect(url_for('auth.login'))
    arts = db.session.query(TbArt).filter(
        TbArt.artist_art_id == session['user_id']
    ).all()
    return render_template('art/upload_art_page.html', arts=arts)


@user.route('/artist/artwork/delete/<int:art_id>', methods=['POST'])
def delete_artwork(art_id):
    if not login_required('artist'):
        return jsonify({'status': 'error', 'message': 'Not logged in.'})
    art = db.session.query(TbArt).get(art_id)
    if art and art.artist_art_id == session['user_id']:
        db.session.delete(art)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Artwork deleted.'})
    return jsonify({'status': 'error', 'message': 'Artwork not found.'})


@user.route('/artist/artwork/edit/<int:art_id>', methods=['POST'])
def edit_artwork(art_id):
    if not login_required('artist'):
        return jsonify({'status': 'error', 'message': 'Not logged in.'})
    art = db.session.query(TbArt).get(art_id)
    if not art or art.artist_art_id != session['user_id']:
        return jsonify({'status': 'error', 'message': 'Artwork not found.'})

    art.art_title  = request.form.get('title', art.art_title).strip()
    art.art_desc   = request.form.get('description', art.art_desc)
    art.art_price  = float(request.form.get('price', art.art_price))
    art.art_image  = request.form.get('image', art.art_image).strip()
    art.stock_qty  = int(request.form.get('stock_qty', art.stock_qty))
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Artwork updated.'})


@user.route('/artist/orders')
def artist_orders():
    if not login_required('artist'):
        return redirect(url_for('auth.login'))
    orders = db.session.query(OrderPurchase).filter(
        OrderPurchase.artist_ord_id == session['user_id']
    ).order_by(OrderPurchase.order_date.desc()).all()
    return render_template('artist/orders_payment_page.html', orders=orders)


@user.route('/artist/messages')
def artist_messages():
    if not login_required('artist'):
        return redirect(url_for('auth.login'))
    messages = db.session.query(MessageChat).filter(
        (MessageChat.sender_id   == session['user_id']) |
        (MessageChat.receiver_id == session['user_id'])
    ).order_by(MessageChat.message_date.desc()).all()
    return render_template('other_features/messages_page.html', messages=messages)


# ─────────────────────────────────────────
# PATRON PAGES
# ─────────────────────────────────────────
@user.route('/patron/dashboard')
def patron_dashboard():
    if not login_required('patron'):
        return redirect(url_for('auth.login'))
    patron = db.session.query(TbPatron).get(session['user_id'])
    orders = db.session.query(OrderPurchase).filter(
        OrderPurchase.patron_ord_id == session['user_id']
    ).order_by(OrderPurchase.order_date.desc()).limit(5).all()
    arts   = db.session.query(TbArt).filter(
        TbArt.artwork_status == 'available'
    ).order_by(TbArt.art_date.desc()).limit(6).all()
    return render_template('patron/patron_dashboard.html',
                           patron=patron, orders=orders, arts=arts)


@user.route('/patron/profile')
def patron_profile():
    if not login_required('patron'):
        return redirect(url_for('auth.login'))
    patron = db.session.query(TbPatron).get(session['user_id'])
    return render_template('patron/patron_profile_page.html', patron=patron)


@user.route('/patron/orders')
def patron_orders():
    if not login_required('patron'):
        return redirect(url_for('auth.login'))
    orders = db.session.query(OrderPurchase).filter(
        OrderPurchase.patron_ord_id == session['user_id']
    ).order_by(OrderPurchase.order_date.desc()).all()
    return render_template('patron/patron_orders.html', orders=orders)


@user.route('/patron/messages')
def patron_messages():
    if not login_required('patron'):
        return redirect(url_for('auth.login'))
    messages = db.session.query(MessageChat).filter(
        (MessageChat.sender_id   == session['user_id']) |
        (MessageChat.receiver_id == session['user_id'])
    ).order_by(MessageChat.message_date.desc()).all()
    return render_template('patron/patron_chat_messages.html', messages=messages)


# ─────────────────────────────────────────
# SEND MESSAGE (AJAX) - shared
# ─────────────────────────────────────────
@user.route('/messages/send', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in.'})

    receiver_id   = request.form.get('receiver_id')
    receiver_type = request.form.get('receiver_type')
    msg_text      = request.form.get('message', '').strip()

    if not all([receiver_id, receiver_type, msg_text]):
        return jsonify({'status': 'error', 'message': 'Missing fields.'})

    new_msg = MessageChat(
        sender_id=session['user_id'],
        sender_type=session['user_type'],
        receiver_id=int(receiver_id),
        receiver_type=receiver_type,
        message_text=msg_text,
        message_date=datetime.utcnow(),
        is_read=False
    )
    db.session.add(new_msg)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Message sent.'})


# ─────────────────────────────────────────
# ART BROWSING PAGES
# ─────────────────────────────────────────
@user.route('/art/listing')
def art_listing():
    arts = db.session.query(TbArt).filter(
        TbArt.artwork_status == 'available'
    ).order_by(TbArt.art_date.desc()).all()
    art_types = db.session.query(TbArtType).all()
    return render_template('art/artwork_listing.html', arts=arts, art_types=art_types)


@user.route('/art/category')
def art_category():
    art_types = db.session.query(TbArtType).all()
    arts      = db.session.query(TbArt).filter(
        TbArt.artwork_status == 'available'
    ).all()
    return render_template('art/artwork_category.html', art_types=art_types, arts=arts)


@user.route('/art/detail/<int:art_id>')
def art_detail(art_id):
    art     = db.session.query(TbArt).get_or_404(art_id)
    artist  = db.session.query(TbArtist).get(art.artist_art_id)
    ratings = db.session.query(RatingReview).filter(
        RatingReview.rated_art_id == art_id
    ).all()
    similar = db.session.query(TbArt).filter(
        TbArt.art_type_id == art.art_type_id,
        TbArt.art_id      != art_id,
        TbArt.artwork_status == 'available'
    ).limit(3).all()
    return render_template('art/artwork_detail.html',
                           art=art, artist=artist,
                           ratings=ratings, similar=similar)


@user.route('/art/search')
def art_search():
    q         = request.args.get('q', '').strip()
    category  = request.args.get('category', '')
    min_price = request.args.get('min_price', 0, type=float)
    max_price = request.args.get('max_price', 999999, type=float)

    query = db.session.query(TbArt).filter(TbArt.artwork_status == 'available')

    if q:
        query = query.filter(TbArt.art_title.like(f'%{q}%'))
        # Save search to history
        if 'user_id' in session:
            track = UserSearchTrack(
                artist_id=session['user_id'] if session.get('user_type') == 'artist' else None,
                patron_id=session['user_id'] if session.get('user_type') == 'patron' else None,
                search_term=q,
                search_date=datetime.utcnow()
            )
            db.session.add(track)
            db.session.commit()

    if category:
        art_type = db.session.query(TbArtType).filter(
            TbArtType.art_type_name == category
        ).first()
        if art_type:
            query = query.filter(TbArt.art_type_id == art_type.art_type_id)

    query = query.filter(TbArt.art_price >= min_price, TbArt.art_price <= max_price)
    arts  = query.all()

    art_types = db.session.query(TbArtType).all()
    return render_template('art/browse_search_page.html',
                           arts=arts, art_types=art_types,
                           query=q, category=category)


# ─────────────────────────────────────────
# RATINGS (AJAX)
# ─────────────────────────────────────────
@user.route('/ratings')
def ratings_page():
    ratings = db.session.query(RatingReview).order_by(
        RatingReview.rating_date.desc()
    ).all()
    return render_template('other_features/ratings&review.html', ratings=ratings)


@user.route('/ratings/submit', methods=['POST'])
def submit_rating():
    if not login_required('patron'):
        return jsonify({'status': 'error', 'message': 'Only patrons can rate.'})

    artist_id = request.form.get('artist_id')
    art_id    = request.form.get('art_id')
    score     = request.form.get('score', type=int)

    if not artist_id or not score:
        return jsonify({'status': 'error', 'message': 'Missing fields.'})
