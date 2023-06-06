import requests
import json


# def predict_rub_salary():


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
    if i == 'Python':
        response = requests.get(url, params=payload)
        response.raise_for_status()
        python_salary = response.json()['items']
        for i in python_salary:
            print(i['salary'])
        # with open("python_salary.txt", "w") as file:
        #     json.dump(python_salary, file)
    response = requests.get(url, params=payload)
    response.raise_for_status()
    hh = response.json()['found']
    vacancies_language[i] = hh
for key, value in vacancies_language.items():
    print(key, value)
# program_language['Python'] = hh
# print(program_language[1])
# for i in hh:
#     print(i['name'])
# with open("hh.txt", "w") as file:
#     json.dump(hh, file)
