from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from pkg.models import db, TbArtist, TbPatron, TbAdmin
from pkg.forms import RegistrationForm
from datetime import datetime
import hashlib

auth = Blueprint('auth', __name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password, hashed):
    return hashlib.sha256(password.encode()).hexdigest() == hashed

@auth.route('/')
def index():
    return render_template('auth_pages/index.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    # If user is already logged in, redirect them
    if 'user_id' in session:
        if session.get('user_type') == 'artist':
            return redirect(url_for('user.artist_dashboard'))
        elif session.get('user_type') == 'patron':
            return redirect(url_for('user.patron_dashboard'))
            
    form = RegistrationForm()
    
    # If it's a GET request, just render the page
    if request.method == 'GET':
        return render_template('auth_pages/register.html', form=form)
    
    # Handle POST request (AJAX)
    if form.validate_on_submit():
        # Extract data from the form
        fname = form.fullname.data.strip().split(' ')[0]
        lname = ' '.join(form.fullname.data.strip().split(' ')[1:])
        email = form.email.data.strip()
        password = form.password.data
        user_type = form.user_type.data
        
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
            
            session['user_id'] = new_user.artist_id
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
                patron_type='buyer',
                patron_regdate=datetime.utcnow()
            )
            db.session.add(new_user)
            db.session.commit()
            
            session['user_id'] = new_user.patron_id
            session['user_type'] = 'patron'
            session['user_name'] = f'{fname} {lname}'
            session['user_email'] = email
            
            return jsonify({'status': 'success', 'redirect': url_for('user.patron_dashboard')})
    
    # Validation failed - return JSON errors
    errors = {}
    for field, field_errors in form.errors.items():
        errors[field] = field_errors[0]  # Only send the first error per field
    
    return jsonify({
        'status': 'error',
        'message': 'Please correct the errors below.',
        'errors': errors
    })

@auth.route('/login', methods=['GET'])
def login():
    # If user is already logged in, redirect them
    if 'user_id' in session:
        if session.get('user_type') == 'artist':
            return redirect(url_for('user.artist_dashboard'))
        elif session.get('user_type') == 'patron':
            return redirect(url_for('user.patron_dashboard'))
            
    return render_template('auth_pages/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    
    if not email or not password:
        return jsonify({'status': 'error', 'message': 'Email and password are required.'})
    
    artist = db.session.query(TbArtist).filter(TbArtist.artist_mail == email).first()
    if artist and check_password(password, artist.artist_password):
        session['user_id'] = artist.artist_id
        session['user_type'] = 'artist'
        session['user_name'] = f'{artist.artist_fname} {artist.artist_lname}'
        session['user_email'] = artist.artist_mail
        return jsonify({'status': 'success', 'redirect': url_for('user.artist_dashboard')})
    
    patron = db.session.query(TbPatron).filter(TbPatron.patron_mail == email).first()
    if patron and check_password(password, patron.patron_password):
        session['user_id'] = patron.patron_id
        session['user_type'] = 'patron'
        session['user_name'] = f'{patron.patron_fname} {patron.patron_lname}'
        session['user_email'] = patron.patron_mail
        return jsonify({'status': 'success', 'redirect': url_for('user.patron_dashboard')})
    
    return jsonify({'status': 'error', 'message': 'Invalid email or password.'})

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.index'))