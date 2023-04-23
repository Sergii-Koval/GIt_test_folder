import requests

def get_news(api_key):
    url = f"https://newsapi.org/v2/top-headlines?country=pl&apiKey={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()["articles"]
    else:
        return []


def get_weather_data(api_key, cities):
    weather_data = []
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    for city in cities:
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric',
            'lang': 'en'
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            weather_data.append(response.json())

    return weather_data
