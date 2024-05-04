from . import app, db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from .models import User, Event, Booking
from faker import Faker
import random
from datetime import datetime, timedelta

booking = Booking(user_id=1, event_id=1, booked_on=datetime.now(), is_paid=False)
db.session.add(booking)
db.session.commit()