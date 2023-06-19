import os
from itertools import count

import requests
from dotenv import find_dotenv, load_dotenv
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
        if vacancy_hh['salary']:
            salary_from_hh = vacancy_hh['salary']['from']
            salary_to_hh = vacancy_hh['salary']['to']
            average_salary_hh += predict_salary(salary_from_hh, salary_to_hh)
            count_vacancy += 1
    try:
        return count_vacancy, average_salary_hh // count_vacancy
    except ZeroDivisionError:
        return count_vacancy, 'Salary didn`t find'


def predict_rub_salary_sj(vacancies_sj):
    count_vacancy = 0
    average_salary_sj = 0
    for vacancy_sj in vacancies_sj:
        salary_from_sj = vacancy_sj['payment_from']
        salary_to_sj = vacancy_sj['payment_to']
        average_salary_sj += predict_salary(salary_from_sj, salary_to_sj)
        count_vacancy += 1
    try:
        return count_vacancy, average_salary_sj // count_vacancy
    except ZeroDivisionError:
        return count_vacancy, 'Salary didn`t find'


def make_table_hh(vacancies_hh):
    vacancies_hh_table = []
    table_headers = [
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата',
        ]
    vacancies_hh_table.append(table_headers)
    for language, vacancy_information in vacancies_hh.items():
        vacancies_hh_table.append(
            [
                language,
                vacancy_information.get('vacancies_found'),
                vacancy_information.get('vacancies_processed'),
                vacancy_information.get('average_salary'),
            ]
        )
    table = AsciiTable(vacancies_hh_table)
    table.title = 'HeadHunter Moscow'
    return table.table


def make_table_sj(vacancies_sj):
    vacancies_sj_table = []
    table_headers = [
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата',
        ]
    vacancies_sj_table.append(table_headers)
    for language, vacancy_information in vacancies_sj.items():
        vacancies_sj_table.append(
            [
                language,
                vacancy_information.get('vacancies_found'),
                vacancy_information.get('vacancies_processed'),
                vacancy_information.get('average_salary'),
            ]
        )
    table = AsciiTable(vacancies_sj_table)
    table.title = 'SuperJob Moscow'
    return table.table


def main():
    load_dotenv(find_dotenv())
    sj_key = os.environ.get("SUPERJOB_KEY")
    popular_languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C']
    vacancies_language_hh = {}
    vacancies_hh = []
    moskva_id = 1
    amount_of_days = 30
    max_pages_hh = 20
    amount_of_vacancies_on_page = 100
    for program_language in popular_languages:
        for page in count(0):
            page_payload_hh = {'pages_number': max_pages_hh, 'page': page}
            payload = {
                'area': moskva_id,
                'period': amount_of_days,
                'text': program_language,
                'per_page': amount_of_vacancies_on_page
            }
            url_hh = 'https://api.hh.ru/vacancies'
            response = requests.get(url_hh, params=payload)
            response.raise_for_status()
            vacancies_hh.append([program_language, response.json()])
            if page >= page_payload_hh['pages_number']:
                break
    for language, vacancy_hh_description in vacancies_hh:
        vacancies_items = vacancy_hh_description['items']
        vacancies_found = vacancy_hh_description['found']
        vacancies_processed, average_salary = predict_rub_salary_hh(vacancies_items)
        salary_hh_statistics = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': vacancies_processed,
            'average_salary': average_salary,
        }
        vacancies_language_hh[language] = salary_hh_statistics
    print(make_table_hh(vacancies_language_hh))

    vacancies_language_sj = {}
    vacancies_sj = []
    headers_sj = {
        'X-Api-App-Id': sj_key,
    }

    publication_period = 0  # 0- all time
    max_number_of_results = 100
    max_pages_sj = 5

    for program_language_sj in popular_languages:
        for page in count(0):
            page_payload_sj = {'pages_number': max_pages_sj, 'page': page}
            payload_sj = {
                'town': 'Москва',
                'count': max_number_of_results,
                'period': publication_period,
                'keyword': program_language_sj
            }
            url_sj = 'https://api.superjob.ru/2.0/vacancies'
            response_sj = requests.get(
                url_sj,
                headers=headers_sj,
                params=payload_sj
                )
            response_sj.raise_for_status()
            vacancies_sj.append([program_language_sj, response_sj.json()])
            if page >= page_payload_sj['pages_number']:
                break
    for language, vacancy_sj_description in vacancies_sj:
        vacancies_sj_objects = vacancy_sj_description['objects']
        vacancies_found_sj = vacancy_sj_description['total']
        vacancies_processed, average_salary = predict_rub_salary_sj(vacancies_sj_objects)
        salary_sj_statistics = {
            'vacancies_found': vacancies_found_sj,
            'vacancies_processed': vacancies_processed,
            'average_salary': average_salary,
        }
        vacancies_language_sj[language] = salary_sj_statistics
    print(make_table_sj(vacancies_language_sj))


if __name__ == '__main__':
    main()
