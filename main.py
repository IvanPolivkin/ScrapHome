# (ссылка на статью) link_job = bloko-link
#
# (зарплата) salary = bloko-header-section-2
#
# (Имя компании) company = vacancy-serp-item__meta-info-company
#
# (город) city = vacancy-serp-item__info
#
# список вакансий = vacancy-serp-content
#

import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

keywords = ['Django', 'Flask']

headers_generator = Headers(os="win", browser="opera")

response = requests.get(url='https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers= headers_generator.generate())
html_data = response.text
soup = BeautifulSoup(html_data, features='lxml')
print(html_data)


link_job = soup.find_all(class_="vacancy-serp-content")
descriptions = soup.find_all(class_="vacancy-description")

if response.status_code == 200:
    results = []
    for link in link_job:
        links_relative = link.find("a", class_="bloko-link")
        links_absolute = f'https://adsrv.hh.ru{links_relative}'
        salary_relative = link.find(class_='bloko-header-section-2')
        company = link.find(class_='vacancy-serp-item__meta-info-company').text
        city = link.find(class_='vacancy-serp-item__info').text
        if salary_relative:
            salary_relative = salary_relative.text.strip()
        else:
            salary_relative = 'Не указана'

        for descrip in descriptions:
            description = descriptions.find(class_='row-content').text
            if any(keyword.lower() in description.lower() for keyword in keywords):
                information = {
                    'link': links_absolute,
                    'company': company,
                    'city': city,
                    'salary': salary_relative
                }
                results.append(information)

        with open('vacancies.json', 'w', encoding='utf-8') as file:
            json.dump(results, file, ensure_ascii=False, indent=4)

    print('Парсинг завершен. Результаты сохранены в файле vacancies.json.')
else:
    print('Ошибка при выполнении запроса.')