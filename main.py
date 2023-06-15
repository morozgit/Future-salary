import requests
from collections import Counter
from terminaltables import AsciiTable
import os
from dotenv import load_dotenv, find_dotenv
from itertools import count


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
        if vacancy_hh['salary'] is not None:
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


def make_table_hh(vacancies_hh):
    table_hh = []
    table_headers = [
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата',
        'Опыт',
        'Занятость'
        ]
    table_hh.append(table_headers)
    for language, vacancy_information in vacancies_hh.items():
        table_hh.append(
            [
                language,
                vacancy_information.get('vacancies_found'),
                vacancy_information.get('vacancies_processed'),
                vacancy_information.get('average_salary'),
                vacancy_information.get('common_experience'),
                vacancy_information.get('common_employment')
            ]
        )
    table = AsciiTable(table_hh)
    table.title = 'HeadHunter Moscow'
    return table.table


def make_table_sj(vacancies_sj):
    table_data = []
    table_headers = [
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата',
        ]
    table_data.append(table_headers)
    for language, vacancy_information in vacancies_sj.items():
        table_data.append(
            [
                language,
                vacancy_information.get('vacancies_found'),
                vacancy_information.get('vacancies_processed'),
                vacancy_information.get('average_salary'),
            ]
        )
    table = AsciiTable(table_data)
    table.title = 'SuperJob Moscow'
    return table.table


def main():
    load_dotenv(find_dotenv())
    sj_key = os.environ.get("SUPERJOB_KEY")
    popular_languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C']
    vacancies_language = {}
    vacancies_hh = []
    moskva_id = 1
    amount_of_days = 30
    max_pages = 2
    for page in count(0):
        for program_language in popular_languages:
            page_payload = {'pages_number': max_pages, 'page': page}
            payload = {
                'area': moskva_id,
                'period': amount_of_days,
                'text': program_language,
            }
            url_hh = 'https://api.hh.ru/vacancies'
            response = requests.get(url_hh, params=payload)
            response.raise_for_status()
            vacancies_hh.append(response.json())
            for vacancy_hh in vacancies_hh:
                vacancies_items = vacancy_hh['items']
                vacancies_found = vacancy_hh['found']
                vacancies_processed = vacancy_hh['per_page']
                vacancies_hh_info = {
                    'vacancies_found': vacancies_found,
                    'vacancies_processed': vacancies_processed,
                    'average_salary': predict_rub_salary_hh(vacancies_items),
                    'common_experience': learn_about_experience(vacancies_items),
                    'common_employment': learn_about_employment(vacancies_items),
                }
                vacancies_language[program_language] = vacancies_hh_info
        # print(vacancies_language)
        
        if page >= page_payload['pages_number']:
            break
    print(make_table_hh(vacancies_language))
    
        

    # vacancies_language_sj = {}
    # headers_superjob = {
    #     'X-Api-App-Id': sj_key,
    # }

    # publication_period = 0  #all time
    # max_number_of_results = 100
    # for program_language_sj in popular_languages:
    #     payload_superjob = {
    #         'town': 'Москва',
    #         'count': max_number_of_results,
    #         'period': publication_period,
    #         'keyword': program_language_sj
    #     }
    #     url_sj = 'https://api.superjob.ru/2.0/vacancies'
    #     response_superjob = requests.get(url_sj, headers=headers_superjob, params=payload_superjob)
    #     response_superjob.raise_for_status()
    #     vacancies_sj = response_superjob.json()
    #     vacancies_sj_objects = vacancies_sj['objects']
    #     vacancies_found_sj = vacancies_sj['total']
    #     vacancies_sj_info_ = {
    #         'vacancies_found': vacancies_found_sj,
    #         'vacancies_processed': payload_superjob['count'],
    #         'average_salary': predict_rub_salary_sj(vacancies_sj_objects),
    #     }
    #     vacancies_language_sj[program_language_sj] = vacancies_sj_info_
    # print(make_table_sj(vacancies_language_sj))


if __name__ == '__main__':
    main()
