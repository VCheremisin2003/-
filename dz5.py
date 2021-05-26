from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from pprint import pprint
from pymongo import MongoClient
driver = webdriver.Chrome()

import time
url = 'https://light.mail.ru/'

driver.get(url)
time.sleep(2)
elem = driver.find_element_by_xpath("//input[@name = 'username']")
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.ENTER)

elem = driver.find_element_by_xpath("//input[@name = 'password']")
time.sleep(1)
elem.send_keys('NextPassword172!')
elem.send_keys(Keys.ENTER)
time.sleep(3)
links = []
while True:
    mes = driver.find_elements_by_xpath("//td[@class='messageline__subject messageline__item']/a[@class='messageline__link']")
    for item in mes:
        link = item.get_attribute('href')
        links.append(link)
    try:
        driver.find_element_by_xpath("//a[@title='Далее']").click()
    except:
        break

mail_masseges = []

for link in links:
    driver.get(link)
    time.sleep(2)
    from_user = driver.find_element_by_xpath("//tr[@class = 'm-header mh-From']//span").text

    date = driver.find_element_by_xpath("//div[@class = 'mr_read__date']/span/span").text
    main_text = driver.find_element_by_xpath("//div[@id = 'msgFieldSubject']/span").text
    text = driver.find_element_by_xpath("//div[contains(@class,'cl_')]").text
    mail = {}
    mail[text] = text
    mail[main_text] = main_text
    mail[date] = date
    mail[from_user] = from_user
    mail_masseges.append(mail)

client = MongoClient('localhost', 27017)
db = client['vacancies_db']
masseges = db.masseges
#запишем в нашу бд полученный словарь
for i in mail_masseges:
    masseges.insert_one(i)





