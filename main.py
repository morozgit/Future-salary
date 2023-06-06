import requests
import json


def predict_rub_salary(vacancie):
    url = 'https://api.hh.ru/vacancies?text={0}'.format(vacancie)
    response = requests.get(url, params=payload)
    response.raise_for_status()
    salary = response.json()['items']
    for i in salary:
        print(i['salary'])


program_language = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C']
vacancies_language = {}
payload = {
    # "text": "Python",
    "area": "1",
    "period": "30",
    # "per_page": 1,  
    }
# url = 'https://api.hh.ru/suggests/vacancy_positions?text=программист'
for i in program_language:
    url = 'https://api.hh.ru/vacancies?text={0}'.format(i)
        # with open("python_salary.txt", "w") as file:
        #     json.dump(python_salary, file)
    response = requests.get(url, params=payload)
    response.raise_for_status()
    hh = response.json()['found']
    print(i)
    vacancies_language[i] = hh
for key, value in vacancies_language.items():
    print(key, value)

predict_rub_salary('Python')
# program_language['Python'] = hh
# print(program_language[1])
# for i in hh:
#     print(i['name'])
# with open("hh.txt", "w") as file:
#     json.dump(hh, file)
