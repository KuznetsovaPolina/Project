# EventBooker: Web-приложение бронирования и условной продажи билетов на массовые мероприятия

## Описание проекта

EventBooker - это веб-приложение, разработанное на Flask, которое предоставляет базовые функции для бронирования билетов на массовые мероприятия. 

## Доска Miro

https://miro.com/app/board/uXjVKE-CtYo=/?share_link_id=170924894457
![Project](https://github.com/KuznetsovaPolina/Project/assets/94856108/96a76486-3a53-4192-9eac-a45e326b593b)


**Основные возможности:**

* Регистрация и вход пользователей с хешированием паролей для обеспечения безопасности.
* Генерация данных о мероприятиях и площадках с использованием генеративных сервисов для создания реалистичных синтетических данных.
* Логика бронирования, реализованная на клиент-серверной архитектуре, с имитацией процесса оплаты (заглушка).
* Система оценок и учет предпочтений пользователей для персонализации.
* Поиск и фильтрация мероприятий по жанрам, рейтингу и локациям.

## Инструкция по запуску (Через bash)

### 1. Установка библиотек

1. **Создание виртуального окружения:**
   python -m venv venv

Активация виртуального окружения:

Windows:

venv/Scripts/activate

macOS/Linux:

source venv/bin/activate

Установка зависимостей:

pip install -r requirements.txt

2. Запуск приложения

Запуск сервера:

python run.py

Доступ к приложению: Откройте веб-браузер и перейдите по адресу http://127.0.0.1:5000/.

## Дополнительная информация

Генерация событий: Для создания новых событий используйте маршрут /generate_events.

Удаление событий: Для удаления всех событий и бронирований используйте маршрут /events_delete.

Поиск и фильтрация: Используйте форму поиска на главной странице для поиска и фильтрации событий.

Реализация системы оплаты. (Заглушка)

Интеграция с API сторонних сервисов для получения актуальной информации о мероприятиях.

Разработка мобильного приложения.

Расширение функционала личного кабинета пользователя.

## Скриншоты, демонстрирующие работу проекта.:

![image](https://github.com/KuznetsovaPolina/Project/assets/107554629/e451d229-aab7-4a21-878e-f35f3e9d00a5)
![image](https://github.com/KuznetsovaPolina/Project/assets/107554629/a2d9241b-2794-45a1-8147-e03fdc8d5792)
![image](https://github.com/KuznetsovaPolina/Project/assets/107554629/ce395acc-a3a4-4a40-bbaa-29fb5c0c5b1a)
![image](https://github.com/KuznetsovaPolina/Project/assets/107554629/292663a1-8d06-4e69-8d6c-1970dcf2c435)
![image](https://github.com/KuznetsovaPolina/Project/assets/107554629/e9fde44d-6548-4556-92ca-27d75945c67a)
![image](https://github.com/KuznetsovaPolina/Project/assets/107554629/ac6a6719-5a6d-4796-ad4f-50224328a3dd)






