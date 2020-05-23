# -*- coding: utf-8 -*-
"""
Created on Tue May 19 00:47:40 2020

@author: hshyu
"""

from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver

# 코로나 확진자 현황
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('lang=ko_KR')

url = 'http://ncov.mohw.go.kr/'
driver = webdriver.Chrome(r'C:\Users\hshyu\ChromeWebDriver\chromedriver.exe', chrome_options=chrome_options)
driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html)

corona_confirmed = soup.find('span', class_='num').text
corona_increase = soup.find('span', class_='sub_num red').text
print('==========================')
print('코로나 확진 현황')
print(corona_confirmed, corona_increase, end='\n')
driver.close()