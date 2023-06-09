import requests
import json


def predict_rub_salary(vacancy):    
    salary_from = vacancy['salary']['from']
    salary_to = vacancy['salary']['to']
    if salary_from and salary_to:
        return (salary_from + salary_to) // 2
    elif salary_from and salary_to is None:
        return salary_from * 1.2
    elif salary_from is None and salary_to:
        return salary_to * 0.8

    # with open("hh.txt", "w") as file:
#     json.dump(hh, file)
    # if vacancy['salary']['currency'] == 'RUB':
    #     return None
    # else:
    #     salary_from = vacancy['salary']['from']
    #     salary_to = vacancy['salary']['to']
    #     if salary_from:
    #         return salary_from * 0.8
    #     elif salary_to:
    #         return salary_to * 1.2
    #     else:
    #         return (salary_from + salary_to) // 2
    # salary_from = []
    # salary_to = []
    # for salary in vacancie:
    #     print(salary)
        # salary_from = salary['salary']['from']
        # print('salary_from', salary_from)
        # salary_to = salary['salary']['to']
        # print('salary_to', salary_to)
        


popular_languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C']
vacancies_language = {}
payload = {
    # "text": "Python",
    "area": "1",
    "period": "30",
    "only_with_salary": True
    # "per_page": 1,  
    }
# url = 'https://api.hh.ru/suggests/vacancy_positions?text=программист'
# for program_language in popular_languages:
#     url = 'https://api.hh.ru/vacancies?text={0}'.format(program_language)
#         # with open("python_salary.txt", "w") as file:
#         #     json.dump(python_salary, file)
#     response = requests.get(url, params=payload)
#     response.raise_for_status()
#     hh = response.json()['found']
#     # print(i)
    
    # vacancies_language[program_language] = hh
# for key, value in vacancies_language.items():
#     print(key, value)

# for i in vacancie['items']:
    # print(i['salary']['from'])
for program_language in popular_languages:
    url = 'https://api.hh.ru/vacancies?text={0}'.format(program_language)
    response = requests.get(url, params=payload)
    response.raise_for_status()
    vacancies = response.json()['items']
    for vacancy in vacancies:
        # print(predict_rub_salary(vacancy))
        vacancies_language[program_language] = predict_rub_salary(vacancy)
# vacancies_language[program_language] = hh
for key, value in vacancies_language.items():
    print(key, value)
# program_language['Python'] = hh
# print(program_language[1])
# for i in hh:
#     print(i['name'])

