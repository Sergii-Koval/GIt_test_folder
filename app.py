from flask import Flask, render_template, request, redirect, url_for
import json
from utils import get_news

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/news')
def news():
    api_key = "4a1faca4363a44a4acfaa1ed621b1d41"
    news = get_news(api_key)
    return render_template('news.html', news=news)

@app.route('/weather')
def weather():
    return render_template('weather.html')

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