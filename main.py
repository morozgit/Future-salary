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
        vacancies_experience.append(vacancy['experience']['name']) 
    return Counter(vacancies_experience).most_common(1)[0][0]


def learn_about_employment(vacancies):
    vacancies_employment = []
    for vacancy in vacancies:
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


def make_tables_hh(vacancies_dictionary):
    table_data = []
    table_headers = [
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата',
        'Опыт',
        'Занятость'
        ]
    table_data.append(table_headers)
    for key, value in vacancies_dictionary.items():
        table_data.append(
            [
                key,
                value.get('vacancies_found'),
                value.get('vacancies_processed'),
                value.get('average_salary'),
                value.get('common_experience'),
                value.get('common_employment')
            ]
        )
    table = AsciiTable(table_data)
    table.title = 'HeadHunter Moscow'
    print(table.table)


def make_tables_sj(vacancies_dictionary):
    table_data = []
    table_headers = [
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата',
        ]
    table_data.append(table_headers)
    for key, value in vacancies_dictionary.items():
        table_data.append(
            [
                key,
                value.get('vacancies_found'),
                value.get('vacancies_processed'),
                value.get('average_salary'),
            ]
        )
    table = AsciiTable(table_data)
    table.title = 'SuperJob Moscow'
    print(table.table)


popular_languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C']
vacancies_language = {}

payload = {
    "area": "1",
    "period": "30",
    "only_with_salary": True
    }

for program_language in popular_languages:
    url_hh = 'https://api.hh.ru/vacancies?text={0}'.format(program_language)
    response = requests.get(url_hh, params=payload)
    response.raise_for_status()
    vacancies = response.json()['items']
    vacancies_found = response.json()['found']
    vacancies_processed = response.json()['per_page']
    vacancies_language_info = {
        'vacancies_found': vacancies_found,
        'vacancies_processed': vacancies_processed,
        'average_salary': predict_rub_salary_hh(vacancies),
        'common_experience': learn_about_experience(vacancies),
        'common_employment': learn_about_employment(vacancies),
    }
    vacancies_language[program_language] = vacancies_language_info
make_tables_hh(vacancies_language)


vacancies_language_sj = {}
headers_superjob = {
    'X-Api-App-Id': 'v3.r.137607251.df77642eb68e4b4b46da5d068879be4074f84b7d.6c814ae2df04a6e77f5fe989615bbe172a3317b2',
}

payload_superjob = {
    'town': 'Москва',
    'count': 100,
    'period': 0
}
for program_language_sj in popular_languages:
    url_sj = 'https://api.superjob.ru/2.0/vacancies/?keyword={0}'.format(program_language_sj)
    response_superjob = requests.get(url_sj, headers=headers_superjob, params=payload_superjob)
    response_superjob.raise_for_status()
    s = response_superjob.json()
    vacancies_sj = response_superjob.json()['objects']
    vacancies_found_sj = response_superjob.json()['total']
    vacancies_language_info_sj = {
        'vacancies_found': vacancies_found_sj,
        'vacancies_processed': payload_superjob['count'],
        'average_salary': predict_rub_salary_sj(vacancies_sj),
    }
    vacancies_language_sj[program_language_sj] = vacancies_language_info_sj
make_tables_sj(vacancies_language_sj)


