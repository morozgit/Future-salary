import os
import time
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


def predict_rub_salary_hh(vacancy_hh):
    salaries_hh = 0
    salary_from_hh = vacancy_hh['salary']['from']
    salary_to_hh = vacancy_hh['salary']['to']
    salaries_hh = predict_salary(salary_from_hh, salary_to_hh)
    return salaries_hh


def predict_rub_salary_sj(vacancy_sj):
    salaries_sj = 0
    salary_from_sj = vacancy_sj['payment_from']
    salary_to_sj = vacancy_sj['payment_to']
    salaries_sj = predict_salary(salary_from_sj, salary_to_sj)
    return salaries_sj


def make_table(vacancies, title):
    vacancies_table = []
    table_headers = [
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата',
        ]
    vacancies_table.append(table_headers)
    for language, vacancy_information in vacancies.items():
        vacancies_table.append(
            [
                language,
                vacancy_information.get('vacancies_found'),
                vacancy_information.get('vacancies_processed'),
                vacancy_information.get('average_salary'),
            ]
        )
    table = AsciiTable(vacancies_table)
    table.title = title
    return table.table


def main():
    load_dotenv(find_dotenv())
    sj_key = os.environ.get("SUPERJOB_KEY")
    popular_languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C']
    vacancies_language_hh = {}
    vacancies_hh = []
    salaries_hh = []
    moskva_id = 1
    amount_of_days = 30
    max_pages_hh = 20
    amount_of_vacancies_on_page = 50
    title_hh = 'HeadHunter Moscow'
    title_sj = 'SuperJob Moscow'
    headers_hh = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    for program_language in popular_languages:
        vacancies_hh_found = 0
        average_hh_salary = 0
        vacancies_hh_processed = 0
        vacancies_hh.clear()
        salaries_hh.clear()
        for page in count(0):
            payload = {
                'area': moskva_id,
                'period': amount_of_days,
                'text': program_language,
                'per_page': amount_of_vacancies_on_page,
                'page': page
            }
            url_hh = 'https://api.hh.ru/vacancies'
            response = requests.get(url_hh, headers=headers_hh, params=payload)
            response.raise_for_status()
            vacancies_hh.append(response.json())
            if page >= max_pages_hh:
                break
            time.sleep(2)
        for page_with_hh_vacancies in vacancies_hh:
            vacancies_items = page_with_hh_vacancies['items']
            vacancies_hh_found = page_with_hh_vacancies['found']
            for vacancy_hh in vacancies_items:
                if vacancy_hh['salary']:
                    salaries_hh.append(predict_rub_salary_hh(vacancy_hh))
        try:
            average_hh_salary = sum(salaries_hh) // len(salaries_hh)
        except ZeroDivisionError:
            average_hh_salary = 0
        vacancies_hh_processed = len(salaries_hh)
        salary_hh_statistics = {
                'vacancies_found': vacancies_hh_found,
                'vacancies_processed': vacancies_hh_processed,
                'average_salary': average_hh_salary,
            }
        vacancies_language_hh[program_language] = salary_hh_statistics

    print(make_table(vacancies_language_hh, title_hh))

    vacancies_language_sj = {}
    vacancies_sj = []
    salaries_sj = []
    headers_sj = {
        'X-Api-App-Id': sj_key,
    }

    publication_period = 0  # 0- all time
    max_number_of_results = 100
    max_pages_sj = 5

    for program_language_sj in popular_languages:
        vacancies_sj_found = 0
        average_sj_salary = 0
        vacancies_sj_processed = 0
        vacancies_sj.clear()
        salaries_sj.clear()
        for page in count(0):
            payload_sj = {
                'town': 'Москва',
                'count': max_number_of_results,
                'period': publication_period,
                'keyword': program_language_sj,
                'page': page
            }
            url_sj = 'https://api.superjob.ru/2.0/vacancies'
            response_sj = requests.get(
                url_sj,
                headers=headers_sj,
                params=payload_sj
                )
            response_sj.raise_for_status()
            vacancies_sj.append(response_sj.json())
            if page >= max_pages_sj:
                break
        for page_with_sj_vacancies in vacancies_sj:
            vacancies_sj_objects = page_with_sj_vacancies['objects']
            vacancies_sj_found = page_with_sj_vacancies['total']
            for vacancy_sj in vacancies_sj_objects:
                if vacancy_sj['payment_from'] != 0 or vacancy_sj['payment_to'] != 0:
                    salaries_sj.append(predict_rub_salary_sj(vacancy_sj))
        try:
            average_sj_salary = sum(salaries_sj) // len(salaries_sj)
        except ZeroDivisionError:
            average_sj_salary = 0
        vacancies_sj_processed = len(salaries_sj)
        salary_sj_statistics = {
            'vacancies_found': vacancies_sj_found,
            'vacancies_processed': vacancies_sj_processed,
            'average_salary': average_sj_salary,
        }
        vacancies_language_sj[program_language_sj] = salary_sj_statistics
    print(make_table(vacancies_language_sj, title_sj))


if __name__ == '__main__':
    main()
