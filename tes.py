import requests

url = "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=cdf42d910fc7411c8b80b187c4fc0431"
r = requests.get(url)
print(r.status_code)
print(r.json())
