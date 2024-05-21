# EventBooker: MVP для бронирования билетов на мероприятия

## Описание проекта

EventBooker - это веб-приложение, разработанное на Flask, которое предоставляет базовые функции для бронирования билетов на массовые мероприятия. 

**Основные возможности:**

* Регистрация и вход пользователей с хешированием паролей для обеспечения безопасности.
* Генерация данных о мероприятиях и площадках с использованием генеративных сервисов для создания реалистичных синтетических данных.
* Логика бронирования, реализованная на клиент-серверной архитектуре, с имитацией процесса оплаты (заглушка).
* Система оценок и учет предпочтений пользователей для персонализации.
* Поиск и фильтрация мероприятий по жанрам, рейтингу и локациям.

## Инструкция по запуску

### 1. Установка библиотек

1. **Создание виртуального окружения:**
   python -m venv venv

Активация виртуального окружения:

Windows:

venv\Scripts\activate

macOS/Linux:

source venv/bin/activate

Установка зависимостей:

pip install -r requirements.txt
2. Настройка базы данных

Создание базы данных:

flask db init
flask db migrate
flask db upgrade

3. Запуск приложения

Запуск сервера:

flask run

Доступ к приложению: Откройте веб-браузер и перейдите по адресу http://127.0.0.1:5000/.

Дополнительная информация

Генерация событий: Для создания новых событий используйте маршрут /generate_events.

Удаление событий: Для удаления всех событий и бронирований используйте маршрут /events_delete.

Поиск и фильтрация: Используйте форму поиска на главной странице для поиска и фильтрации событий.

Будущее развитие

Реализация полноценной системы оплаты.

Интеграция с API сторонних сервисов для получения актуальной информации о мероприятиях.

Разработка мобильного приложения.

Расширение функционала личного кабинета пользователя.