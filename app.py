from flask import Flask, render_template, request, redirect, url_for
import json
from utils import get_news, search_movie, get_weather_data
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return render_template('index.html', now=now)

@app.route('/search_movie', methods=['POST'])
def search():
    api_key = '71b74252366bfdee35930c6b3e0ada0b'
    movie_title = request.form['movie_title']
    movie_results = search_movie(api_key, movie_title)
    return render_template('index.html', movie_results=movie_results)

@app.route('/news')
def news():
    api_key = "4a1faca4363a44a4acfaa1ed621b1d41"
    news = get_news(api_key)
    return render_template('news.html', news=news)

@app.route('/weather')
def weather():
    api_key = 'ee3a5b3e2579c460393c5bd95f670bca'
    cities = ['Warsaw', 'Minsk', 'Batumi']
    weather_data = get_weather_data(api_key, cities)
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


if __name__ == '__main__':
    app.run(debug=True)