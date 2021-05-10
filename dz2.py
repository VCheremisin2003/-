from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

#сначала разделим введённую вакансию плюсами

VName = str(input())
d = VName.split(' ')
b = ''
l = 1
for item in d:
    b = b + item
    if l < len(d):
        b = b + '+'
    l += 1

#далее найдём сколько страниц вакансий на сайте

k = 0
ln = 1
while ln > 0:
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    url = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=' + b + '&from=suggest_post&page=' + str(k)
    response = requests.get(url, headers=headers)
    dom = bs(response.text,'html.parser')
    vacancy_list = dom.find_all('div',{'class': 'vacancy-serp-item'})
    ln = len(vacancy_list)
    k += 1

vacancies = []

#для каждого номера страницы откроем её

for page_number in range(0, k):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    url = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=' + b + '&from=suggest_post&page=' + str(k)
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
        #Запишем данные в словарь
        vacancies.append(vacancy_data)

print(vacancies)

