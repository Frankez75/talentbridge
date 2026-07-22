from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, flash
from pkg.models import db, TbPatron, TbArt, OrderPurchase, OrderPurchaseDetail, Payment
from datetime import datetime
import random
import string

transaction = Blueprint('transaction', __name__)


def login_required_patron():
    """Check if user is a logged-in patron."""
    if 'user_id' not in session or session.get('user_type') != 'patron':
        return False
    return True


def generate_order_id():
    """Generate a unique order ID."""
    prefix = "ORD"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{prefix}-{timestamp}-{random_suffix}"


def generate_tracking_number():
    """Generate a random tracking number."""
    return "TRK" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


# ─────────────────────────────────────────
# CHECKOUT PAGE
# ─────────────────────────────────────────
@transaction.route('/checkout')
def checkout():
    if not login_required_patron():
        flash('Please sign in to complete your purchase.', 'warning')
        return redirect(url_for('auth.login', redirect='checkout'))
    
    # Get artwork from URL parameter
    art_id = request.args.get('art_id')
    art = None
    if art_id:
        art = db.session.query(TbArt).get(art_id)
        if not art or art.artwork_status != 'available':
            flash('Artwork not available.', 'error')
            return redirect(url_for('main.artwork_listing'))
    
    return render_template('transaction/checkout_order.html', art=art)


# ─────────────────────────────────────────
# PAYMENT PAGE
# ─────────────────────────────────────────
@transaction.route('/payment')
def payment():
    if not login_required_patron():
        return redirect(url_for('auth.login'))
    
    art_id = request.args.get('art_id')
    art = db.session.query(TbArt).get_or_404(art_id) if art_id else None
    
    if not art or art.artwork_status != 'available':
        flash('Artwork not available for purchase.', 'error')
        return redirect(url_for('main.artwork_listing'))
    
    return render_template('transaction/payment.html', art=art)


# ─────────────────────────────────────────
# PLACE ORDER (AJAX)
# ─────────────────────────────────────────
@transaction.route('/api/order/create', methods=['POST'])
def create_order():
    if not login_required_patron():
        return jsonify({'status': 'error', 'message': 'Please sign in.'})
    
    art_id = request.form.get('art_id')
    shipping_name = request.form.get('shipping_name', '').strip()
    shipping_email = request.form.get('shipping_email', '').strip()
    shipping_address = request.form.get('shipping_address', '').strip()
    shipping_city = request.form.get('shipping_city', '').strip()
    shipping_state = request.form.get('shipping_state', '').strip()
    shipping_zip = request.form.get('shipping_zip', '').strip()
    shipping_country = request.form.get('shipping_country', '').strip()
    payment_method = request.form.get('payment_method', 'card')
    
    if not all([art_id, shipping_name, shipping_email, shipping_address, shipping_city, shipping_state, shipping_zip, shipping_country]):
        return jsonify({'status': 'error', 'message': 'Please fill in all required shipping fields.'})
    
    art = db.session.query(TbArt).get(art_id)
    if not art or art.artwork_status != 'available':
        return jsonify({'status': 'error', 'message': 'Artwork not available.'})
    
    try:
        # Create Order
        order_id = generate_order_id()
        delivery_address = f"{shipping_address}, {shipping_city}, {shipping_state} {shipping_zip}, {shipping_country}"
        
        new_order = OrderPurchase(
            patron_ord_id=session['user_id'],
            artist_ord_id=art.artist_art_id,
            total_amount=art.art_price,
            order_status='pending',
            delivery_address=delivery_address
        )
        db.session.add(new_order)
        db.session.flush()  # Get the order_id
        
        # Create Order Detail
        new_detail = OrderPurchaseDetail(
            purchase_amt=art.art_price,
            order_status='pending',
            order_id=new_order.order_id,
            art_item_id=art.art_id,
            stock_quantity=1
        )
        db.session.add(new_detail)
        
        # Create Payment record
        payment_ref = "PAY-" + datetime.now().strftime("%Y%m%d%H%M%S") + ''.join(random.choices(string.digits, k=4))
        new_payment = Payment(
            patron_payment_id=session['user_id'],
            order_art_id=new_order.order_id,
            artist_payment_id=art.artist_art_id,
            payment_reference=payment_ref,
            amount_payed=art.art_price,
            payment_status='pending'
        )
        db.session.add(new_payment)
        
        # Update artwork stock
        art.stock_qty -= 1
        if art.stock_qty <= 0:
            art.artwork_status = 'sold'
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'order_id': new_order.order_id,
            'message': 'Order created successfully!'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating order: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred. Please try again.'})


# ─────────────────────────────────────────
# ORDER CONFIRMATION
# ─────────────────────────────────────────
@transaction.route('/order/confirmation')
def order_confirmation():
    order_id = request.args.get('order_id')
    if not order_id:
        return redirect(url_for('main.artwork_listing'))
    
    order = db.session.query(OrderPurchase).get(order_id)
    if not order:
        flash('Order not found.', 'error')
        return redirect(url_for('main.artwork_listing'))
    
    return render_template('transaction/order_confirmation.html', order=order)


# ─────────────────────────────────────────
# PATRON ORDERS
# ─────────────────────────────────────────
@transaction.route('/patron/orders')
def patron_orders():
    if not login_required_patron():
        return redirect(url_for('auth.login'))
    
    orders = db.session.query(OrderPurchase).filter(
        OrderPurchase.patron_ord_id == session['user_id']
    ).order_by(OrderPurchase.order_date.desc()).all()
    
    return render_template('patron/patron_orders.html', orders=orders)


# ─────────────────────────────────────────
# PATRON ORDERS DATA (JSON for AJAX)
# ─────────────────────────────────────────
@transaction.route('/api/patron/orders')
def patron_orders_data():
    if not login_required_patron():
        return jsonify({'status': 'error', 'message': 'Not logged in.'})
    
    orders = db.session.query(OrderPurchase).filter(
        OrderPurchase.patron_ord_id == session['user_id']
    ).order_by(OrderPurchase.order_date.desc()).all()
    
    data = [{
        'id': o.order_id,
        'artworkTitle': o.details[0].art_item.art_title if o.details else 'Unknown',
        'artworkId': o.details[0].art_item.art_id if o.details else None,
        'artistName': f"{o.artist_buyer.artist_fname} {o.artist_buyer.artist_lname}" if o.artist_buyer else 'Unknown',
        'artistId': o.artist_ord_id,
        'image': o.details[0].art_item.art_image if o.details else None,
        'amount': float(o.total_amount),
        'status': o.order_status.title(),
        'orderDate': o.order_date.strftime('%Y-%m-%d') if o.order_date else None,
        'processingDate': None,  # You can add these fields to your model
        'shippedDate': None,
        'deliveredDate': None,
        'reviewed': False
    } for o in orders]
    
    return jsonify({'orders': data})


# ─────────────────────────────────────────
# ARTIST ORDERS (Sales)
# ─────────────────────────────────────────
@transaction.route('/artist/orders')
def artist_orders():
    if 'user_id' not in session or session.get('user_type') != 'artist':
        return redirect(url_for('auth.login'))
    
    orders = db.session.query(OrderPurchase).filter(
        OrderPurchase.artist_ord_id == session['user_id']
    ).order_by(OrderPurchase.order_date.desc()).all()
    
    return render_template('transaction/orders_payment_page.html', orders=orders)


# ─────────────────────────────────────────
# ARTIST ORDERS DATA (JSON for AJAX)
# ─────────────────────────────────────────
@transaction.route('/api/artist/orders')
def artist_orders_data():
    if 'user_id' not in session or session.get('user_type') != 'artist':
        return jsonify({'status': 'error', 'message': 'Not logged in.'})
    
    orders = db.session.query(OrderPurchase).filter(
        OrderPurchase.artist_ord_id == session['user_id']
    ).order_by(OrderPurchase.order_date.desc()).all()
    
    data = [{
        'id': o.order_id,
        'artworkTitle': o.details[0].art_item.art_title if o.details else 'Unknown',
        'artworkImage': o.details[0].art_item.art_image if o.details else None,
        'buyerName': f"{o.patron_buyer.patron_fname} {o.patron_buyer.patron_lname}" if o.patron_buyer else 'Unknown',
        'buyerEmail': o.patron_buyer.patron_mail if o.patron_buyer else None,
        'amount': float(o.total_amount),
        'status': o.order_status.title(),
        'orderDate': o.order_date.strftime('%Y-%m-%d') if o.order_date else None,
        'processingDate': None,
        'shippedDate': None,
        'deliveredDate': None
    } for o in orders]
    
    return jsonify({'orders': data})


# ─────────────────────────────────────────
# TRACK ORDER (AJAX)
# ─────────────────────────────────────────
@transaction.route('/api/order/track/<int:order_id>')
def track_order(order_id):
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in.'})
    
    order = db.session.query(OrderPurchase).get(order_id)
    if not order:
        return jsonify({'status': 'error', 'message': 'Order not found.'})
    
    # Check if user has permission to track this order
    user_id = session['user_id']
    user_type = session.get('user_type')
    
    if (user_type == 'patron' and order.patron_ord_id != user_id) or \
       (user_type == 'artist' and order.artist_ord_id != user_id):
        return jsonify({'status': 'error', 'message': 'Access denied.'})
    
    # Build timeline
    timeline = []
    timeline.append({
        'label': 'Order Placed',
        'date': order.order_date.strftime('%Y-%m-%d %H:%M:%S') if order.order_date else None,
        'completed': True
    })
    
    # Check status progression
    statuses = ['pending', 'processing', 'shipped', 'delivered', 'completed']
    for status in statuses:
        if order.order_status == status:
            timeline.append({
                'label': status.title(),
                'date': order.order_date.strftime('%Y-%m-%d %H:%M:%S'),
                'completed': True
            })
            break
    
    return jsonify({'status': 'success', 'timeline': timeline})