from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from .models import User, Event, Booking
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        user_preferences = current_user.preferences.split(',') if current_user.preferences else []
        preferred_events = Event.query.filter(Event.genre.in_(user_preferences)).all()
        other_events = Event.query.filter(Event.genre.notin_(user_preferences)).all()
        events = preferred_events + other_events
    else:
        events = Event.query.all()
    return render_template('home.html', events=events)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        preferences = request.form.get('preferences', '') # Получение предпочтений
        try:
            hashed_password = generate_password_hash(password)
            user = User(username=username, password_hash=hashed_password, preferences=preferences)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful!')
        except Exception as e:
            db.session.rollback()
            flash(str(e))
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out.')
    return redirect(url_for('home'))

@app.route('/generate_events')
def generate_events():
    # Удаление всех существующих мероприятий
    Event.query.delete()

    # Генерация новых мероприятий с использованием генеративных сервисов
    events = []
    genres = ['Concert', 'Festival', 'Theater', 'Exhibition', 'Sport']
    for _ in range(10):  # Генерация 10 новых мероприятий
        event_name = fake.text(max_nb_chars=50)  # Название мероприятия
        location = fake.city()  # Место проведения мероприятия
        date = datetime.now() + timedelta(days=random.randint(1, 30))  # Дата проведения мероприятия
        genre = random.choice(genres) # Случайный выбор жанра
        rating = round(random.uniform(0, 5), 1) # Случайный рейтинг
        events.append({'name': event_name, 'location': location, 'date': date, 'genre': genre, 'rating': rating})

    db.session.bulk_insert_mappings(Event, events)
    db.session.commit()
    flash('All existing events were deleted and new events were generated!')
    return redirect(url_for('home'))

@app.route('/book/<int:event_id>', methods=['GET', 'POST'])
@login_required
def book(event_id):
    event = Event.query.get_or_404(event_id)
    try:
        booking = Booking(user_id=current_user.id, event_id=event.id)
        db.session.add(booking)
        db.session.commit()
        flash('You have successfully booked a ticket!')
    except Exception as e:
        db.session.rollback()
        flash('Error booking the event: ' + str(e))
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # Ensure any failed database sessions don't interfere with access
    return render_template('500.html'), 500


@app.route('/payment/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def payment(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if request.method == 'POST':
        # Здесь может быть логика обработки платежных данных (заглушка)
        booking.is_paid = True
        db.session.commit()
        flash('Payment processed successfully.', 'success')
        return redirect(url_for('home'))
    
    return render_template('payment.html', booking=booking)

@app.route('/events_delete') 
def events_delete():
    # Удаление всех существующих мероприятий
    Event.query.delete()
    Booking.query.delete()
    events = []
    books = []
    db.session.bulk_insert_mappings(Event, events)
    db.session.bulk_insert_mappings(Booking, books)
    db.session.commit()
    flash('Events & books delete!')
    return redirect(url_for('home'))
    
@app.route('/bookings')
@login_required
def bookings():
    bookings = Booking.query.join(Event).filter(Booking.user_id == current_user.id, Event.id != None).all()
    return render_template('bookings.html', bookings=bookings)

@app.route('/search')
def search():
    query = request.args.get('query', '')
    genre = request.args.get('genre', '')
    min_rating = request.args.get('min_rating', 0, type=float)
    location = request.args.get('location', '')

    events = Event.query
    if query:
        events = events.filter(Event.name.ilike(f'%{query}%'))
    if genre:
        events = events.filter_by(genre=genre)
    if min_rating:
        events = events.filter(Event.rating >= min_rating)
    if location:
        events = events.filter(Event.location.ilike(f'%{location}%'))
    events = events.all()

    return render_template('home.html', events=events)