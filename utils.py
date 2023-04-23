import requests

def get_news(api_key):
    url = f"https://newsapi.org/v2/top-headlines?country=pl&apiKey={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()["articles"]
    else:
        return []
