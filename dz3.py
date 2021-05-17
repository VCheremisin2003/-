from pymongo import MongoClient
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

print('введите название вакансии:')
b = str(input())
print('введите желаемую зарплату:')
price = int(input())
client = MongoClient('localhost', 27017)
db = client['vacancies_db']
vaccol = db.vacancies

#далее найдём сколько страниц вакансий на сайте
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
url = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=' + b + '&from=suggest_post&page=0'
response = requests.get(url, headers=headers)
dom = bs(response.text, 'html.parser')
vacancy_list = dom.find_all('a', {'class': 'bloko-button'})
number = int(vacancy_list[-2].text)

vacancies = []

#для каждого номера страницы откроем её
for page_number in range(0, number):
    url = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=' + b + '&from=suggest_post&page=' + str(page_number)
    response = requests.get(url, headers=headers)
    dom = bs(response.text, 'html.parser')
    vacancy_list = dom.find_all('div', {'class': 'vacancy-serp-item'})
#для каждой вакансии найдём нужную информацию
    for vacancy in vacancy_list:
        vacancy_data = {}
        vacancy_name = vacancy.find('a', {'class': 'bloko-link'}).text
        vacancy_link = vacancy.find('a', {'class': 'bloko-link'})['href']
        vacancy_salary = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText()
        vacancy_owner = vacancy.find('a', {'class': 'bloko-link_secondary'})['href']
        vs = vacancy_salary.split(' ')
        max_price = None
        min_price = None
        currency = None
        #для зарплаты переведём её в нормальный вид, ибо там какая-то хрень в середине, типа \u202f
        if len(vs) == 3 and vs[0] == 'до':
            max_price = vs[1]
            min_price = None
            currency = str(vs[2])
            mp = max_price.split('\u202f')
            max_price = int(mp[0] + mp[1])
        if len(vs) == 3 and vs[0] == 'от':
            max_price = None
            min_price = vs[1]
            currency = str(vs[2])
            mp = min_price.split('\u202f')
            min_price = int(mp[0] + mp[1])
        if len(vs) == 4:
            max_price = vs[2]
            min_price = vs[0]
            currency = str(vs[3])
            mp = max_price.split('\u202f')
            max_price = int(mp[0] + mp[1])
            mp = min_price.split('\u202f')
            min_price = int(mp[0] + mp[1])
        vacancy_data['vacancy_name'] = vacancy_name
        vacancy_data['vacancy_link'] = vacancy_link
        vacancy_data['vacancy_owner'] = vacancy_owner
        vacancy_data['max_salary'] = max_price
        vacancy_data['min_salary'] = min_price
        vacancy_data['currancy'] = currency
        #сделаем ключ id ссылкой на вакансию, чтобы отслежтивать повторение вакансий
        vacancy_data['_id'] = vacancy_link
        #Запишем данные в словарь
        vacancies.append(vacancy_data)



client = MongoClient('localhost', 27017)
db = client['vacancies_db']
vaccol = db.vacancies
#запишем в нашу бд полученный словарь
for i in vacancies:
    vaccol.insert_one(i)
#найдём вакансии, где минимальная и максимальная зп больше нашей суммы
norm_vacancies = vaccol.find( { '$or': [ { 'min_salary': { '$gt': price } }, { 'max_salary': { '$gt': price } } ] } )
for i in norm_vacancies:
    pprint(i)

def NewVacancies():
    for page_number in range(0, 1):
        url = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=' + b + '&from=suggest_post&page=' + str(
            page_number)
        response = requests.get(url, headers=headers)
        dom = bs(response.text, 'html.parser')
        vacancy_list = dom.find_all('div', {'class': 'vacancy-serp-item'})
        # для каждой вакансии найдём нужную информацию
        for vacancy in vacancy_list:
            listv = []
            vacancy_data = {}
            vacancy_name = vacancy.find('a', {'class': 'bloko-link'}).text
            vacancy_link = vacancy.find('a', {'class': 'bloko-link'})['href']
            vacancy_salary = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText()
            vacancy_owner = vacancy.find('a', {'class': 'bloko-link_secondary'})['href']
            vs = vacancy_salary.split(' ')
            max_price = None
            min_price = None
            currency = None
            # для зарплаты переведём её в нормальный вид, ибо там какая-то хрень в середине, типа \u202f
            if len(vs) == 3 and vs[0] == 'до':
                max_price = vs[1]
                min_price = None
                currency = str(vs[2])
                mp = max_price.split('\u202f')
                max_price = int(mp[0] + mp[1])
            if len(vs) == 3 and vs[0] == 'от':
                max_price = None
                min_price = vs[1]
                currency = str(vs[2])
                mp = min_price.split('\u202f')
                min_price = int(mp[0] + mp[1])
            if len(vs) == 4:
                max_price = vs[2]
                min_price = vs[0]
                currency = str(vs[3])
                mp = max_price.split('\u202f')
                max_price = int(mp[0] + mp[1])
                mp = min_price.split('\u202f')
                min_price = int(mp[0] + mp[1])
            vacancy_data['vacancy_name'] = vacancy_name
            vacancy_data['vacancy_link'] = vacancy_link
            vacancy_data['vacancy_owner'] = vacancy_owner
            vacancy_data['max_salary'] = max_price
            vacancy_data['min_salary'] = min_price
            vacancy_data['currancy'] = currency
            vacancy_data['_id'] = vacancy_link
            # Запишем данные в словарь
            listv.append(vacancy_data)
            k = 0
            #проврим на отсутвии вакансии в нашей бд
            for i in vaccol.find({}):
                if vacancy_link == i('_id'):
                    k = 1
            if k == 0:
                #если её нет - запишем в бд
                vaccol.insert_one(listv[0])



