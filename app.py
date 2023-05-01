from flask import Flask, render_template, request, redirect, url_for
import json
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

if __name__ == '__main__':
    app.run(debug=True)
