import requests
import json


payload = {
    "text": "Python OR Java",
    "area": "1",
    "period": "30",
    # "per_page": 1,
    
    }
# url = 'https://api.hh.ru/suggests/vacancy_positions?text=программист'
url = 'https://api.hh.ru/vacancies'
response = requests.get(url, params=payload)
response.raise_for_status()
hh = response.json()['found']
print(hh)
# for i in hh:
#     print(i['name'])
# with open("hh.txt", "w") as file:
#     json.dump(hh, file)
