import requests
import json
from collections import Counter
from terminaltables import AsciiTable


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) // 2
    elif salary_from and (salary_to is None or salary_to == 0):
        return salary_from * 1.2
    elif (salary_from is None or salary_to == 0) and salary_to:
        return salary_to * 0.8
    else:
        return 0


def predict_rub_salary_hh(vacancies_hh):
    count_vacancy = 0
    average_salary_hh = 0
    for vacancy_hh in vacancies_hh:
        salary_from_hh = vacancy_hh['salary']['from']
        salary_to_hh = vacancy_hh['salary']['to']
        average_salary_hh += predict_salary(salary_from_hh, salary_to_hh)
        count_vacancy += 1
    try:
        return average_salary_hh // count_vacancy
    except ZeroDivisionError:
        return 'Salary didn`t find'


def learn_about_experience(vacancies):
    vacancies_experience = []
    for vacancy in vacancies:
        # print(vacancy.most_common(1))
        # print(max([vacancy.count(x) for x in set(vacancy['experience']['name'])]))
        vacancies_experience.append(vacancy['experience']['name']) 
    return Counter(vacancies_experience).most_common(1)[0][0]


def learn_about_employment(vacancies):
    vacancies_employment = []
    for vacancy in vacancies:
        # print(vacancy.most_common(1))
        # print(max([vacancy.count(x) for x in set(vacancy['experience']['name'])]))
        vacancies_employment.append(vacancy['employment']['name']) 
    return Counter(vacancies_employment).most_common(1)[0][0]


def predict_rub_salary_sj(vacancies_sj):
    count_vacancy = 0
    average_salary_sj = 0
    for vacancy_sj in vacancies_sj:
        salary_from_sj = vacancy_sj['payment_from']
        salary_to_sj = vacancy_sj['payment_to']
        average_salary_sj += predict_salary(salary_from_sj, salary_to_sj)
        count_vacancy += 1
    try:
        return average_salary_sj // count_vacancy
    except ZeroDivisionError:
        return 'Salary didn`t find'
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
# vacancies_info = ['vacancies_found', 'vacancies_processed', 'average_salary']
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
#     response = requests.get(url, params=payload)
#     response.raise_for_status()
#     hh = response.json()
#     with open("python_salary.txt", "w") as file:
#         json.dump(hh, file)
    
    # vacancies_language[program_language] = hh
# for key, value in vacancies_language.items():
#     print(key, value)

# for i in vacancie['items']:
    # print(i['salary']['from'])
    
for program_language in popular_languages:
    url_hh = 'https://api.hh.ru/vacancies?text={0}'.format(program_language)
    response = requests.get(url_hh, params=payload)
    response.raise_for_status()
    vacancies = response.json()['items']
    vacancies_found = response.json()['found']
    vacancies_processed = response.json()['per_page']
    # print(predict_rub_salary(vacancies))
    vacancies_language_info = {
        'vacancies_found': vacancies_found,
        'vacancies_processed': vacancies_processed,
        'average_salary': predict_rub_salary_hh(vacancies),
        'common experience': learn_about_experience(vacancies),
        'common employment': learn_about_employment(vacancies),
    }
    vacancies_language[program_language] = vacancies_language_info
#     for vacancy in vacancies:
#         # vacancies_language[program_language] = predict_rub_salary(vacancy)
#         for quantity in vacancies_info:
#         # print(predict_rub_salary(vacancy))
#             vacancies_language_info[quantity] = count_vacancies
#         vacancies_language[program_language] = vacancies_language_info
# # vacancies_language[program_language] = hh
for key, value in vacancies_language.items():
    table = AsciiTable(value)
    print(table.table)

# program_language['Python'] = hh
# print(program_language[1])
# for i in hh:
#     print(i['name'])
print('superjob')
vacancies_language_sj = {}
headers_superjob = {
    'X-Api-App-Id': 'v3.r.137607251.df77642eb68e4b4b46da5d068879be4074f84b7d.6c814ae2df04a6e77f5fe989615bbe172a3317b2',
}

payload_superjob = {
    # 'keyword': 'Программист',
    'town': 'Москва',
    'count': 100
}
# url_superjob = 'https://api.superjob.ru/2.0/favorites'
# response_superjob = requests.post(url_superjob, json=payload_superjob)
# url_superjob = 'https://api.superjob.ru/2.0/vacancies/'
# response_superjob = requests.get(url_superjob, headers=headers_superjob, params=payload_superjob)
# response_superjob.raise_for_status()
# vacancies_sj = response.json()['items']
# print(predict_rub_salary_sj(vacancies_sj))
for program_language_sj in popular_languages:
    url_sj = 'https://api.superjob.ru/2.0/vacancies/?keyword={0}'.format(program_language_sj)
    response_superjob = requests.get(url_sj, headers=headers_superjob, params=payload_superjob)
    response_superjob.raise_for_status()
    s = response_superjob.json()
    with open("{0}.txt".format(program_language_sj), "w") as file:
        json.dump(s, file)
    vacancies_sj = response_superjob.json()['objects']
    vacancies_found_sj = response_superjob.json()['total']
    # vacancies_processed_sj = response_superjob.json()['per_page']
    # print(predict_rub_salary(vacancies))
    vacancies_language_info_sj = {
        'vacancies_found': vacancies_found_sj,
        'vacancies_processed': payload_superjob['count'],
        'average_salary': predict_rub_salary_sj(vacancies_sj),
        # 'common experience': learn_about_experience(vacancies),
        # 'common employment': learn_about_employment(vacancies),
    }
    vacancies_language_sj[program_language_sj] = vacancies_language_info_sj
#     for vacancy in vacancies:
#         # vacancies_language[program_language] = predict_rub_salary(vacancy)
#         for quantity in vacancies_info:
#         # print(predict_rub_salary(vacancy))
#             vacancies_language_info[quantity] = count_vacancies
#         vacancies_language[program_language] = vacancies_language_info
# # vacancies_language[program_language] = hh
for key, value in vacancies_language_sj.items():
    print(key, value)


