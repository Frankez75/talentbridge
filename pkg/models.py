from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# ─────────────────────────────────────────
# STATE
# ─────────────────────────────────────────
class State(db.Model):
    __tablename__ = 'state'

    state_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state_name = db.Column(db.String(100), nullable=False)

    artists = db.relationship('TbArtist', backref='state', lazy=True)
    patrons = db.relationship('TbPatron', backref='state', lazy=True)

    def __repr__(self):
        return f'<State {self.state_name}>'


# ─────────────────────────────────────────
# TB_ARTISTS
# ─────────────────────────────────────────
class TbArtist(db.Model):
    __tablename__ = 'tb_artists'

    artist_id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artist_fname    = db.Column(db.String(100), nullable=False)
    artist_lname    = db.Column(db.String(100), nullable=False)
    artist_phone    = db.Column(db.String(200), nullable=True)
    artist_mail     = db.Column(db.String(100), nullable=False, unique=True)
    artist_password = db.Column(db.String(255), nullable=False)
    artist_bio      = db.Column(db.String(1000), nullable=True)
    artist_art      = db.Column(db.String(200), nullable=True)
    artist_reg_date = db.Column(db.DateTime, default=datetime.utcnow)
    artist_state_id = db.Column(db.Integer, db.ForeignKey('state.state_id'), nullable=True)

    arts = db.relationship('TbArt', backref='artist', lazy=True)
    sent_messages = db.relationship(
        'MessageChat',
        foreign_keys='MessageChat.sender_id',
        backref='sender_artist', lazy=True
    )
    ratings_received = db.relationship(
        'RatingReview',
        foreign_keys='RatingReview.rated_artist_id',
        backref='rated_artist', lazy=True
    )
    artist_orders = db.relationship(
        'OrderPurchase',
        foreign_keys='OrderPurchase.artist_ord_id',
        backref='artist_buyer', lazy=True
    )
    artist_payments = db.relationship(
        'Payment',
        foreign_keys='Payment.artist_payment_id',
        backref='artist_payer', lazy=True
    )
    search_history = db.relationship(
        'UserSearchTrack',
        foreign_keys='UserSearchTrack.artist_id',
        backref='searching_artist', lazy=True
    )

    def __repr__(self):
        return f'<Artist {self.artist_fname} {self.artist_lname}>'


# ─────────────────────────────────────────
# TB_PATRONS
# ─────────────────────────────────────────
class TbPatron(db.Model):
    __tablename__ = 'tb_patrons'

    patron_id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patron_fname    = db.Column(db.String(100), nullable=False)
    patron_lname    = db.Column(db.String(100), nullable=False)
    patron_mail     = db.Column(db.String(100), nullable=False, unique=True)
    patron_password = db.Column(db.String(255), nullable=False)
    patron_type     = db.Column(db.Enum('buyer', 'scout', 'business'), nullable=False)
    patron_regdate  = db.Column(db.DateTime, default=datetime.utcnow)
    patron_state_id = db.Column(db.Integer, db.ForeignKey('state.state_id'), nullable=True)

    patron_orders = db.relationship(
        'OrderPurchase',
        foreign_keys='OrderPurchase.patron_ord_id',
        backref='patron_buyer', lazy=True
    )
    patron_payments = db.relationship(
        'Payment',
        foreign_keys='Payment.patron_payment_id',
        backref='patron_payer', lazy=True
    )
    ratings_given = db.relationship(
        'RatingReview',
        foreign_keys='RatingReview.rated_by_id',
        backref='reviewer', lazy=True
    )
    search_history = db.relationship(
        'UserSearchTrack',
        foreign_keys='UserSearchTrack.patron_id',
        backref='searching_patron', lazy=True
    )

    def __repr__(self):
        return f'<Patron {self.patron_fname} {self.patron_lname}>'


# ─────────────────────────────────────────
# TB_ADMIN
# ─────────────────────────────────────────
class TbAdmin(db.Model):
    __tablename__ = 'tb_admin'

    admin_id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_fullname   = db.Column(db.String(150), nullable=False)
    admin_email      = db.Column(db.String(200), nullable=False, unique=True)
    admin_password   = db.Column(db.String(155), nullable=False)
    admin_lastlogged = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Admin {self.admin_fullname}>'


# ─────────────────────────────────────────
# TB_ART_TYPE
# ─────────────────────────────────────────
class TbArtType(db.Model):
    __tablename__ = 'tb_art_type'

    art_type_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    art_type_name = db.Column(db.String(75), nullable=False)

    arts = db.relationship('TbArt', backref='art_type', lazy=True)

    def __repr__(self):
        return f'<ArtType {self.art_type_name}>'


# ─────────────────────────────────────────
# TB_ARTS
# ─────────────────────────────────────────
class TbArt(db.Model):
    __tablename__ = 'tb_arts'

    art_id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    art_title      = db.Column(db.String(100), nullable=False)
    art_desc       = db.Column(db.String(5000), nullable=True)
    art_price      = db.Column(db.Numeric(10, 2), nullable=False)
    art_image      = db.Column(db.String(300), nullable=True)
    art_type_id    = db.Column(db.Integer, db.ForeignKey('tb_art_type.art_type_id'), nullable=True)
    artwork_status = db.Column(db.Enum('available', 'sold', 'reserved'), default='available')
    artist_art_id  = db.Column(db.Integer, db.ForeignKey('tb_artists.artist_id'), nullable=False)
    art_date       = db.Column(db.DateTime, default=datetime.utcnow)
    stock_qty      = db.Column(db.Integer, default=1)

    order_details = db.relationship('OrderPurchaseDetail', backref='art_item', lazy=True)
    ratings = db.relationship(
        'RatingReview',
        foreign_keys='RatingReview.rated_art_id',
        backref='rated_art', lazy=True
    )

    def __repr__(self):
        return f'<Art {self.art_title}>'


# ─────────────────────────────────────────
# ORDERS / PURCHASES
# ─────────────────────────────────────────
class OrderPurchase(db.Model):
    __tablename__ = 'orders_purchases'

    order_id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patron_ord_id    = db.Column(db.Integer, db.ForeignKey('tb_patrons.patron_id'), nullable=True)
    artist_ord_id    = db.Column(db.Integer, db.ForeignKey('tb_artists.artist_id'), nullable=True)
    order_date       = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount     = db.Column(db.Numeric(10, 2), nullable=False)
    order_status     = db.Column(db.Enum('pending', 'completed', 'cancelled'), default='pending')
    delivery_address = db.Column(db.String(500), nullable=True)

    details  = db.relationship('OrderPurchaseDetail', backref='order', lazy=True)
    payments = db.relationship('Payment', backref='order', lazy=True)

    def __repr__(self):
        return f'<Order {self.order_id} - {self.order_status}>'


# ─────────────────────────────────────────
# ORDER / PURCHASE DETAILS
# ─────────────────────────────────────────
class OrderPurchaseDetail(db.Model):
    __tablename__ = 'order_purchase_deta'

    purchase_id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    purchase_amt   = db.Column(db.Numeric(10, 2), nullable=False)
    order_status   = db.Column(db.Enum('pending', 'completed', 'cancelled'), default='pending')
    order_id       = db.Column(db.Integer, db.ForeignKey('orders_purchases.order_id'), nullable=False)
    art_item_id    = db.Column(db.Integer, db.ForeignKey('tb_arts.art_id'), nullable=False)
    stock_quantity = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f'<OrderDetail {self.purchase_id}>'


# ─────────────────────────────────────────
# PAYMENTS
# ─────────────────────────────────────────
class Payment(db.Model):
    __tablename__ = 'payments'

    payment_id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patron_payment_id = db.Column(db.Integer, db.ForeignKey('tb_patrons.patron_id'), nullable=True)
    order_art_id      = db.Column(db.Integer, db.ForeignKey('orders_purchases.order_id'), nullable=False)
    date_payed        = db.Column(db.DateTime, default=datetime.utcnow)
    artist_payment_id = db.Column(db.Integer, db.ForeignKey('tb_artists.artist_id'), nullable=True)
    payment_reference = db.Column(db.String(95), nullable=True, unique=True)
    amount_payed      = db.Column(db.Numeric(10, 2), nullable=False)
    payment_status    = db.Column(db.Enum('pending', 'successful', 'failed'), default='pending')

    def __repr__(self):
        return f'<Payment {self.payment_id} - {self.payment_status}>'


# ─────────────────────────────────────────
# MESSAGES / CHATS
# ─────────────────────────────────────────
class MessageChat(db.Model):
    __tablename__ = 'messages_chats'

    message_id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id     = db.Column(db.Integer, db.ForeignKey('tb_artists.artist_id'), nullable=True)
    sender_type   = db.Column(db.Enum('artist', 'patron'), nullable=False)
    receiver_id   = db.Column(db.Integer, db.ForeignKey('tb_artists.artist_id'), nullable=True)
    receiver_type = db.Column(db.Enum('artist', 'patron'), nullable=False)
    message_text  = db.Column(db.Text, nullable=False)
    message_date  = db.Column(db.DateTime, default=datetime.utcnow)
    is_read       = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Message {self.message_id} from {self.sender_type} {self.sender_id}>'


# ─────────────────────────────────────────
# RATINGS / REVIEWS
# ─────────────────────────────────────────
class RatingReview(db.Model):
    __tablename__ = 'ratings_reviews'

    ratings_id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rating_score    = db.Column(db.SmallInteger, nullable=False)
    rated_artist_id = db.Column(db.Integer, db.ForeignKey('tb_artists.artist_id'), nullable=False)
    rated_art_id    = db.Column(db.Integer, db.ForeignKey('tb_arts.art_id'), nullable=True)
    rated_by_id     = db.Column(db.Integer, db.ForeignKey('tb_patrons.patron_id'), nullable=False)
    rating_date     = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Rating {self.rating_score}★ for Artist {self.rated_artist_id}>'


# ─────────────────────────────────────────
# USER SEARCH TRACK
# ─────────────────────────────────────────
class UserSearchTrack(db.Model):
    __tablename__ = 'user_search_tra'

    user_search_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artist_id      = db.Column(db.Integer, db.ForeignKey('tb_artists.artist_id'), nullable=True)
    patron_id      = db.Column(db.Integer, db.ForeignKey('tb_patrons.patron_id'), nullable=True)
    search_term    = db.Column(db.String(255), nullable=False)
    search_date    = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Search "{self.search_term}">'