from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Создание экземпляра приложения
app = Flask(__name__)

# Конфигурация приложения
app.config['SECRET_KEY'] = 'your-secret-key'  # Замените на ваш реальный секретный ключ
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Или другая база данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключение предупреждений и лишней нагрузки

# Инициализация расширений
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Указываем endpoint для перенаправления на страницу входа

# Импорт маршрутов
from app import routes