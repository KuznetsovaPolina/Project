from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    """Загружает пользователя по его ID.

    Args:
        user_id (int): ID пользователя.

    Returns:
        User: Объект пользователя.
    """
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """Модель пользователя."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    preferences = db.Column(db.String(255))
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def set_password(self, password: str) -> None:
        """Устанавливает пароль пользователя.

        Args:
            password (str): Пароль пользователя.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Проверяет пароль пользователя.

        Args:
            password (str): Пароль для проверки.

        Returns:
            bool: True, если пароль верный, False в противном случае.
        """
        return check_password_hash(self.password_hash, password)

class Event(db.Model):
    """Модель события."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    genre = db.Column(db.String(50)) 
    rating = db.Column(db.Float, default=0.0) 
    bookings = db.relationship('Booking', backref='event', lazy=True, cascade='all, delete-orphan')

class Booking(db.Model):
    """Модель бронирования."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    booked_on = db.Column(db.DateTime, default=datetime.utcnow)
    is_paid = db.Column(db.Boolean, default=False)
