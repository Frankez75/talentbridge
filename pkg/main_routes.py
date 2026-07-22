from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, abort
from pkg.models import db, TbArt, TbArtist, TbArtType, RatingReview, State
from datetime import datetime

main = Blueprint('main', __name__)


# ─────────────────────────────────────────
# HOMEPAGE
# ─────────────────────────────────────────
@main.route('/')
def index():
    # Fetch recent artworks for the homepage
    recent_arts = db.session.query(TbArt).filter(
        TbArt.artwork_status == 'available'
    ).order_by(TbArt.art_date.desc()).limit(6).all()
    
    return render_template('auth_pages/index.html', recent_arts=recent_arts)


# ─────────────────────────────────────────
# ARTWORK LISTING (GALLERY)
# ─────────────────────────────────────────
@main.route('/artwork-listing')
def artwork_listing():
    # Pass art types for the filter dropdown
    art_types = db.session.query(TbArtType).all()
    return render_template('art/artwork_listing.html', art_types=art_types)


# ─────────────────────────────────────────
# ARTWORK DETAIL
# ─────────────────────────────────────────
@main.route('/art/detail/<int:art_id>')
def art_detail(art_id):
    art = db.session.query(TbArt).get_or_404(art_id)
    artist = db.session.query(TbArtist).get(art.artist_art_id)
    
    # Get art type for similar search
    art_type_id = art.art_type_id
    
    similar = db.session.query(TbArt).filter(
        TbArt.art_type_id == art_type_id,
        TbArt.art_id != art_id,
        TbArt.artwork_status == 'available'
    ).limit(4).all()
    
    # Get ratings for this artwork
    ratings = db.session.query(RatingReview).filter(
        RatingReview.rated_art_id == art_id
    ).order_by(RatingReview.rating_date.desc()).all()
    
    return render_template('art/artwork_detail.html',
                           art=art,
                           artist=artist,
                           similar=similar,
                           ratings=ratings)


# ─────────────────────────────────────────
# ARTWORK CATEGORY
# ─────────────────────────────────────────
@main.route('/art/category')
def art_category():
    art_types = db.session.query(TbArtType).all()
    return render_template('art/artwork_category.html', art_types=art_types)


# ─────────────────────────────────────────
# BROWSE / SEARCH (JSON for AJAX)
# ─────────────────────────────────────────
@main.route('/api/artworks/search')
def search_artworks():
    q = request.args.get('q', '').strip()
    category = request.args.get('category', '')
    min_price = request.args.get('min_price', 0, type=float)
    max_price = request.args.get('max_price', 999999, type=float)
    
    query = db.session.query(TbArt).filter(TbArt.artwork_status == 'available')
    
    if q:
        query = query.filter(TbArt.art_title.like(f'%{q}%'))
    
    if category:
        art_type = db.session.query(TbArtType).filter(
            TbArtType.art_type_name == category
        ).first()
        if art_type:
            query = query.filter(TbArt.art_type_id == art_type.art_type_id)
    
    query = query.filter(TbArt.art_price >= min_price, TbArt.art_price <= max_price)
    arts = query.order_by(TbArt.art_date.desc()).all()
    
    # Format data for JSON response
    data = [{
        'id': art.art_id,
        'title': art.art_title,
        'artist': f"{art.artist.artist_fname} {art.artist.artist_lname}" if art.artist else "Unknown",
        'price': float(art.art_price),
        'category': art.art_type.art_type_name if art.art_type else "General",
        'image': art.art_image or "https://placehold.co/600x500/e67300/white?text=Artwork",
        'rating': 4.5,  # Placeholder - would need to calculate average from RatingReview
        'reviews': 0
    } for art in arts]
    
    return jsonify(data)


# ─────────────────────────────────────────
# ARTIST PUBLIC PROFILE
# ─────────────────────────────────────────
@main.route('/artist/<int:artist_id>')
def artist_public_profile(artist_id):
    artist = db.session.query(TbArtist).get_or_404(artist_id)
    artworks = db.session.query(TbArt).filter(
        TbArt.artist_art_id == artist_id,
        TbArt.artwork_status == 'available'
    ).order_by(TbArt.art_date.desc()).all()
    
    # Get orders for sales count
    orders = db.session.query(OrderPurchase).filter(
        OrderPurchase.artist_ord_id == artist_id,
        OrderPurchase.order_status == 'completed'
    ).all()
    
    ratings = db.session.query(RatingReview).filter(
        RatingReview.rated_artist_id == artist_id
    ).all()
    
    # Calculate average rating
    avg_rating = sum([r.rating_score for r in ratings]) / len(ratings) if ratings else 0
    
    return render_template('artist/artist_page(public_facing).html',
                           artist=artist,
                           artworks=artworks,
                           orders=orders,
                           ratings=ratings,
                           avg_rating=avg_rating)


# ─────────────────────────────────────────
# CONTACT ARTIST (AJAX)
# ─────────────────────────────────────────
@main.route('/contact/artist', methods=['POST'])
def contact_artist():
    artist_id = request.form.get('artist_id')
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    subject = request.form.get('subject', '').strip()
    message = request.form.get('message', '').strip()
    
    if not all([artist_id, name, email, message]):
        return jsonify({'status': 'error', 'message': 'All fields are required.'})
    
    # In a real app, you would send an email here or save to a ContactMessage model
    
    return jsonify({'status': 'success', 'message': 'Message sent successfully!'})