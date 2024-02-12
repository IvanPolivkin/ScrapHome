import requests
from bs4 import BeautifulSoup
import json
url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
keywords = ['Django', 'Flask']
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/58.0.3029.110 ',
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    vacancies_list = soup.find('main', class_='vacancy-serp-content')
    vacancies = vacancies_list.find_all('div', class_='serp-item')
    results = []
    for vacancy in vacancies:
        links_relative = vacancy.find("a", class_="bloko-link")
        links_absolute = f'https://adsrv.hh.ru{links_relative}'
        company = vacancy.find(class_='vacancy-serp-item__meta-info-company').text
        city = vacancy.find(attrs={'class': 'bloko-text', 'data-qa': 'vacancy-serp__vacancy-address'}).text
        salary = vacancy.find('span', class_='bloko-header-section-2')
        if salary:
            salary = salary.text.strip()
        else:
            salary = 'Не указана'

        results.append({
            'link': links_absolute,
            'company': company,
            'city': city,
            'salary': salary
        })
        # description = vacancy.find(class_='g-user-content')
        # if any(keyword.lower() in description.lower() for keyword in keywords):
        #     vacancy_info = {
        #         'link': link,
        #         'company': company,
        #         'city': city,
        #         'salary': salary
        #     }
        #     results.append(vacancy_info)

    with open('vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)

    print('Парсинг завершен. Результаты сохранены в файле vacancies.json.')
else:
    print('Ошибка при выполнении запроса.')