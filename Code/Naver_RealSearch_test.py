# -*- coding: utf-8 -*-
"""
Created on Mon May 18 15:12:12 2020

@author: hshyu
"""
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver

# 네이버 실검 크롤링
# 크롬 창 안띄우고 selenium 실행
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('lang=ko_KR')

url = 'https://datalab.naver.com/keyword/realtimeList.naver?where=main'
driver = webdriver.Chrome(r'C:\Users\hshyu\ChromeWebDriver\chromedriver.exe', chrome_options=chrome_options)
driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html)

item_title = soup.select('span.item_title')

print('==============')
num = 1
for i in item_title:
    print(str(num) + '. '  + i.get_text(), end='\n')
    num += 1
    
driver.close()