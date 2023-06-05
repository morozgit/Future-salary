import requests


payload = {
    "text": "программист",
    "area": "1",
    "period": "30"
    }
# url = 'https://api.hh.ru/suggests/vacancy_positions?text=программист'
url = 'https://api.hh.ru/vacancies'
response = requests.get(url, params=payload)
response.raise_for_status()
hh = response.json()
print(hh)
