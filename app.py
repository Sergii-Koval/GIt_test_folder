from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import hashlib
import os
from utils import get_news, search_movie, get_weather_data
from datetime import datetime
from config import movie_api_key, news_api_key, weather_api_key

app = Flask(__name__)

@app.route('/')
def home():
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return render_template('index.html', now=now)

@app.route('/search_movie', methods=['POST'])
def search():
    movie_title = request.form['movie_title']
    movie_results = search_movie(movie_api_key, movie_title)
    return render_template('index.html', movie_results=movie_results)

@app.route('/news')
def news():
    news_data = get_news(news_api_key)
    return render_template('news.html', news=news_data)

@app.route('/weather')
def weather():
    cities = ['Warsaw', 'Minsk', 'Batumi']
    weather_data = get_weather_data(weather_api_key, cities)
    return render_template('weather.html', weather_data=weather_data)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form['name']
    message = request.form['message']

    data = {
        'name': name,
        'message': message
    }

    with open('contacts.json', 'a') as f:
        json.dump(data, f)
        f.write('\n')

    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')

# Load users data from JSON file
def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save users data to JSON file
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

# Hash a password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)
        users = load_users()

        if username in users and hashed_password == users[username]:
            session['user'] = username
            flash('You have successfully logged in.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)
        users = load_users()

        if username not in users:
            users[username] = hashed_password
            save_users(users)
            flash('Your account has been successfully created.', 'success')
            return redirect(url_for('login'))
        else:
            flash('This username is already taken.', 'danger')
            return redirect(url_for('register'))

    return render_template('registration.html')

@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
        flash('You have successfully logged out.', 'success')
    return redirect(url_for('home'))

# Configure Flask secret key for sessions
app.secret_key = os.urandom(24)


if __name__ == '__main__':
    app.run(debug=True)
