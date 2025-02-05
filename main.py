import bs4
import requests
from bs4 import BeautifulSoup
import csv
import time
from  pprint import pprint

base_url = "https://resartis.org/open-calls/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Referer": "https://www.google.com/",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

# def get_headers():
#     return Headers(browser = 'chrome', os = 'win').generate()


with open("result_parsed.csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Записываем заголовки столбцов
    writer.writerow([
        'Title', 'Deadline', 'Country', 'Description', 'Duration', 'Accommodation',
        'Disciplines', 'Studio/Workspace', 'Fees', 'Expectations',
        'Application Information', 'Application Deadline',
        'Residency Starts', 'Residency Ends', 'Location', 'Link'
    ])

    # counter = 0
    try:
        response = requests.get(base_url, headers=headers, timeout=15)
        response.raise_for_status()  # проверка на успешный ответ

    except requests.exceptions.HTTPError as err:
        print(f"HTTP ошибка: {err}")
    except Exception as err:
        print(f"Другая ошибка: {err}")
    else:
        # Парсим HTML-контент
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('div', class_='grid__item postcard')
        print(soup.prettify())

        for item in items:
            # Извлекаем заголовок и ссылку на страницу
            link_tag = item.find('a', href=True)
            link = link_tag['href']
            title = item.find('h2', class_='card__title').get_text(strip=True)

            # Печать ссылки и заголовка для проверки
            print(f"Title: {title}")
            print(f"Link: {link}")

            # Переход по ссылке и парсинг страницы
            detail_response = requests.get(link, headers=headers)
            detail_soup = BeautifulSoup(detail_response.content, 'html.parser')

            # Извлечение данных со страницы
            description = detail_soup.find('div', class_='entry-content').get_text(strip=True)
            deadline = item.find('dt').get_text(strip=True).replace('Deadline: ', '')
            country = deadline.split('Country: ')[1] if 'Country: ' in deadline else ''
            deadline = deadline.split('Country: ')[0] if 'Country: ' in deadline else deadline

            duration = detail_soup.find('h5', text='Duration of residency').find_next('span').get_text(strip=True)
            accommodation = detail_soup.find('h5', text='Accommodation').find_next('span').get_text(strip=True)
            disciplines = detail_soup.find('h5', text='Disciplines, work equipment and assistance').find_next(
                'span').get_text(strip=True)
            studio = detail_soup.find('h5', text='Studio / Workspace').find_next('span').get_text(strip=True)
            fees = detail_soup.find('h5', text='Fees and support').find_next('span').get_text(strip=True)
            expectations = detail_soup.find('h5', text='Expectations towards the artist').find_next('span').get_text(
                strip=True)
            application_info = detail_soup.find('h5', text='Application information').find_next('span').get_text(
                strip=True)

            application_deadline = detail_soup.find('h5', text='Application deadline').find_next('span').get_text(
                strip=True)
            residency_starts = detail_soup.find('h5', text='Residency starts').find_next('span').get_text(strip=True)
            residency_ends = detail_soup.find('h5', text='Residency ends').find_next('span').get_text(strip=True)
            location = detail_soup.find('h5', text='Location').find_next('span').get_text(strip=True)

            more_info_link = detail_soup.find('h5', text='Link to more information').find_next('a', href=True)['href']

            # Записываем данные в CSV-файл
            writer.writerow([
                title, deadline, country, description, duration, accommodation,
                disciplines, studio, fees, expectations, application_info,
                application_deadline, residency_starts, residency_ends, location, more_info_link
            ])
            # counter += 1
            # if counter == 20:
            #     break

print(f"Данные успешно записаны.")
