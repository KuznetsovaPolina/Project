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
def home() -> str:
    """Отображает главную страницу со списком предстоящих событий.

    Returns:
        str: HTML-код главной страницы.
    """
    if current_user.is_authenticated:
        user_preferences = current_user.preferences.split(',') if current_user.preferences else []
        preferred_events = Event.query.filter(Event.genre.in_(user_preferences)).all()
        other_events = Event.query.filter(Event.genre.notin_(user_preferences)).all()
        events = preferred_events + other_events
    else:
        events = Event.query.all()
    return render_template('home.html', events=events)

@app.route('/register', methods=['GET', 'POST'])
def register() -> str:
    """Обрабатывает регистрацию новых пользователей.

    Returns:
        str: HTML-код страницы регистрации или перенаправление на страницу входа после успешной регистрации.
    """
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
def login() -> str:
    """Обрабатывает вход пользователей в систему.

    Returns:
        str: HTML-код страницы входа или перенаправление на главную страницу после успешного входа.
    """
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
def logout() -> str:
    """Выход пользователя из системы.

    Returns:
        str: Перенаправление на главную страницу.
    """
    logout_user()
    flash('You have successfully logged out.')
    return redirect(url_for('home'))

@app.route('/generate_events')
def generate_events() -> str:
    """Генерирует набор случайных событий и сохраняет их в базе данных.

    Returns:
        str: Перенаправление на главную страницу.
    """

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
def book(event_id: int) -> str:
    """Обрабатывает бронирование билета на событие.

    Args:
        event_id (int): ID события.

    Returns:
        str: Перенаправление на главную страницу.
    """
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
def page_not_found(e) -> tuple[str, int]:
    """Обрабатывает ошибку 404 (страница не найдена).

    Args:
        e: Объект ошибки.

    Returns:
        Tuple[str, int]: HTML-код страницы ошибки и код статуса 404.
    """
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error) -> tuple[str, int]:
    """Обрабатывает внутреннюю ошибку сервера (код 500).

    Args:
        error: Объект ошибки.

    Returns:
        Tuple[str, int]: HTML-код страницы ошибки и код статуса 500.
    """
    db.session.rollback() 
    return render_template('500.html'), 500


@app.route('/payment/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def payment(booking_id) -> str:
    """Обрабатывает оплату бронирования.

    Args:
        booking_id (int): ID бронирования.

    Returns:
        str: HTML-код страницы оплаты или перенаправление на главную страницу после успешной оплаты.
    """
    booking = Booking.query.get_or_404(booking_id)
    if request.method == 'POST':
        # Здесь может быть логика обработки платежных данных (заглушка)
        booking.is_paid = True
        db.session.commit()
        flash('Payment processed successfully.', 'success')
        return redirect(url_for('home'))
    
    return render_template('payment.html', booking=booking)

@app.route('/events_delete') 
def events_delete() -> str:
    """Удаляет все события и бронирования из базы данных.

    Returns:
        str: Перенаправление на главную страницу.
    """
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
def bookings() -> str:
    """Отображает страницу с бронированиями текущего пользователя.

    Returns:
        str: HTML-код страницы с бронированиями.
    """
    bookings = Booking.query.join(Event).filter(Booking.user_id == current_user.id, Event.id != None).all()
    return render_template('bookings.html', bookings=bookings)

@app.route('/search')
def search() -> str:
    """Обрабатывает запросы поиска и фильтрации событий.

    Returns:
        str: HTML-код страницы с результатами поиска.
    """
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
    events = events.order_by(Event.rating.desc()).all()
    return render_template('home.html', 
                              events=events, 
                              query=query, 
                              genre=genre, 
                              min_rating=min_rating, 
                              location=location) 