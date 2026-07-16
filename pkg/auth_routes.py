from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from pkg.models import db, TbArtist, TbPatron, TbAdmin
from datetime import datetime
import hashlib

auth = Blueprint('auth', __name__)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(password, hashed):
    return hashlib.sha256(password.encode()).hexdigest() == hashed


# ─────────────────────────────────────────
# INDEX / LANDING
# ─────────────────────────────────────────
@auth.route('/')
def index():
    return render_template('auth_pages/index.html')


# ─────────────────────────────────────────
# REGISTER - GET
# ─────────────────────────────────────────
@auth.route('/register', methods=['GET'])
def register():
    return render_template('auth_pages/register.html')


# ─────────────────────────────────────────
# REGISTER - POST (AJAX)
# ─────────────────────────────────────────
@auth.route('/register', methods=['POST'])
def register_post():
    fname     = request.form.get('fname', '').strip()
    lname     = request.form.get('lname', '').strip()
    email     = request.form.get('email', '').strip()
    password  = request.form.get('password', '')
    user_type = request.form.get('user_type', '')  # 'artist' or 'patron'
    patron_type = request.form.get('patron_type', 'buyer')  # buyer/scout/business

    # Basic validation
    if not all([fname, lname, email, password, user_type]):
        return jsonify({'status': 'error', 'message': 'All fields are required.'})

    if len(password) < 8:
        return jsonify({'status': 'error', 'message': 'Password must be at least 8 characters.'})

    hashed = hash_password(password)

    if user_type == 'artist':
        existing = db.session.query(TbArtist).filter(TbArtist.artist_mail == email).first()
        if existing:
            return jsonify({'status': 'error', 'message': 'Email already registered.'})

        new_user = TbArtist(
            artist_fname=fname,
            artist_lname=lname,
            artist_mail=email,
            artist_password=hashed,
            artist_reg_date=datetime.utcnow()
        )
        db.session.add(new_user)
        db.session.commit()

        session['user_id']   = new_user.artist_id
        session['user_type'] = 'artist'
        session['user_name'] = f'{fname} {lname}'
        session['user_email'] = email

        return jsonify({'status': 'success', 'redirect': url_for('user.artist_dashboard')})

    elif user_type == 'patron':
        existing = db.session.query(TbPatron).filter(TbPatron.patron_mail == email).first()
        if existing:
            return jsonify({'status': 'error', 'message': 'Email already registered.'})

        new_user = TbPatron(
            patron_fname=fname,
            patron_lname=lname,
            patron_mail=email,
            patron_password=hashed,
            patron_type=patron_type,
            patron_regdate=datetime.utcnow()
        )
        db.session.add(new_user)
        db.session.commit()

        session['user_id']   = new_user.patron_id
        session['user_type'] = 'patron'
        session['user_name'] = f'{fname} {lname}'
        session['user_email'] = email

        return jsonify({'status': 'success', 'redirect': url_for('user.patron_dashboard')})

    return jsonify({'status': 'error', 'message': 'Invalid user type.'})


# ─────────────────────────────────────────
# LOGIN - GET
# ─────────────────────────────────────────
@auth.route('/login', methods=['GET'])
def login():
    return render_template('auth_pages/login.html')


# ─────────────────────────────────────────
# LOGIN - POST (AJAX)
# ─────────────────────────────────────────
@auth.route('/login', methods=['POST'])
def login_post():
    email    = request.form.get('email', '').strip()
    password = request.form.get('password', '')

    if not email or not password:
        return jsonify({'status': 'error', 'message': 'Email and password are required.'})

    # Check artist
    artist = db.session.query(TbArtist).filter(TbArtist.artist_mail == email).first()
    if artist and check_password(password, artist.artist_password):
        session['user_id']    = artist.artist_id
        session['user_type']  = 'artist'
        session['user_name']  = f'{artist.artist_fname} {artist.artist_lname}'
        session['user_email'] = artist.artist_mail
        return jsonify({'status': 'success', 'redirect': url_for('user.artist_dashboard')})

    # Check patron
    patron = db.session.query(TbPatron).filter(TbPatron.patron_mail == email).first()
    if patron and check_password(password, patron.patron_password):
        session['user_id']    = patron.patron_id
        session['user_type']  = 'patron'
        session['user_name']  = f'{patron.patron_fname} {patron.patron_lname}'
        session['user_email'] = patron.patron_mail
        return jsonify({'status': 'success', 'redirect': url_for('user.patron_dashboard')})

    return jsonify({'status': 'error', 'message': 'Invalid email or password.'})


# ─────────────────────────────────────────
# LOGOUT
# ─────────────────────────────────────────
@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.index'))