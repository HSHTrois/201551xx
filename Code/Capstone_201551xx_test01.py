from __future__ import print_function
from PIL import Image, ImageTk
from contextlib import contextmanager
from tkinter import *
from urllib.request import urlopen, Request
import urllib
import bs4
import time

import feedparser
# 캘린더 API 
import datetime
import pickle
import os.path

date_format = "%Y년 %m월 %d일"
xlarge_text_size = 88
large_text_size = 42
medium_text_size = 20
small_text_size = 12
locale = 'ko_kr' 
setfont = '맑은 고딕'
DayOfWeek = ['월', '화', '수', '목', '금', '토', '일']
AMPM = {'AM':'오전', 'PM':'오후'}
weather_locale = '춘천시 옥천동' # 네이버 날씨 받아올 곳
hour_4 = 14400000 # 4시간

class Clock(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='black')
        # 시간
        self.time1 = ''
        self.timeLbl = Label(self, font=(setfont, large_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=E)
        
        # 나머지 요일
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=(setfont, small_text_size), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=E)
        
        # 시계 밑에 워터마크
        self.watermark = '\n캡스톤 김휘진 양상열 황승'
        self.watermarkLbl = Label(self, text=self.watermark, font=(setfont, small_text_size, 'bold'), fg="white", bg="black")
        self.watermarkLbl.pack(side=TOP, anchor=E)
        
        # 시간 새로고침, 받아오기
        self.update()

    def update(self):
        time2 = AMPM[time.strftime('%p')] + time.strftime(' %I:%M')
        day_of_week2 = time.strftime(date_format.encode('unicode-escape').decode() + ' ' + DayOfWeek[time.localtime().tm_wday].encode('unicode-escape').decode() + '요일'.encode('unicode-escape').decode()).encode().decode('unicode-escape')
        
        # lable에 현재시간으로 업데이트
        if time2 != self.time1:
            self.time1 = time2
            self.timeLbl.config(text=time2)
        if day_of_week2 != self.day_of_week1:
            self.day_of_week1 = day_of_week2
            self.dayOWLbl.config(text=day_of_week2)
        self.timeLbl.after(200, self.update) # 200ms 새로고침

class Weather(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='black')

        self.weatherContainer = Frame(self, bg="black")
        self.weatherContainer.pack(side=TOP)
        
        self.parsing()
    
    def parsing(self):
        
        # tk 새로고침 위한 destroy()
        for widget in self.weatherContainer.winfo_children():
            widget.destroy()
            print('destroy')
        
        # 네이버에서 파싱
        self.enc_location = urllib.parse.quote(weather_locale + '+날씨')
        
        self.url = 'https://search.naver.com/search.naver?ie=utf8&query='+ self.enc_location
        
        self.req = Request(self.url)
        self.page = urlopen(self.req)
        self.html = self.page.read()
        self.soup = bs4.BeautifulSoup(self.html, 'html5lib')

        # 온도와 날씨정보 긁어오기
        self.temperature = self.soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text + '℃'
        self.weatherinfo = self.soup.find('ul', class_='info_list').find('p', class_='cast_txt').text
        
        #위치
        self.weatherLbl1 = Label(self.weatherContainer, text = weather_locale, font=(setfont, medium_text_size, 'bold'), fg = "white", bg = "black")
        self.weatherLbl1.pack(side=TOP, anchor=W)
        # 온도
        self.weatherLbl2 = Label(self.weatherContainer, text = self.temperature, font=(setfont, large_text_size), fg = "white", bg = "black")
        self.weatherLbl2.pack(side=TOP, anchor=W)
        # 상세정보
        self.weatherLbl3 = Label(self.weatherContainer, text = self.weatherinfo, font=(setfont, small_text_size), fg = "white", bg = "black")
        self.weatherLbl3.pack(side=TOP, anchor=W)
        
        # 날씨 테스트용
        print('============================')
        print('weather update time' + time.strftime(' %I:%M'))
        print(self.temperature)
        print(self.weatherinfo)
        print('============================')
        
        # 4시간마다 업데이트
        self.after(hour_4, self.parsing)

class News(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.config(bg='black')
        self.title = '뉴스'
        self.newsLbl = Label(self, text=self.title, font=(setfont, large_text_size, 'bold'), fg="white", bg="black")
        self.newsLbl.pack(side=TOP, anchor=W)
        self.headlinesContainer = Frame(self, bg="black")
        self.headlinesContainer.pack(side=TOP)
        self.get_headlines()

    def get_headlines(self):
        
        # tk 새로고침 위한 destroy()
        for widget in self.headlinesContainer.winfo_children():
            widget.destroy()
        
        # 구글 rss
        headlines_url = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"     
        feed = feedparser.parse(headlines_url)
                
        for post in feed.entries[0:5]:
            self.headline = Label(self.headlinesContainer, text=post.title, font=(setfont, small_text_size), fg="white", bg="black")
            self.headline.pack(side=TOP, anchor=W)
     
        # 뉴스 테스트용
        print('============================')
        print('headline update time' + time.strftime(' %I:%M'))
        for n in feed.entries[0:5]:
            print(n.title)
            
        # 4시간마다 업데이트
        self.after(hour_4, self.get_headlines)

class FullscreenWindow:
    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        
        self.state = False # 전체화면 우선 False로 설정 후 아래 실행
        self.tk.attributes("-fullscreen", True) # 일단 자동으로 바로 전체화면 뜨게함
        self.tk.bind("<Return>", self.go_fullscreen) # 엔터 누르면 전체화면
        self.tk.bind("<Escape>", self.end_fullscreen) # esc 종료
        
        # 시계
        self.clock = Clock(self.topFrame)
        self.clock.pack(side=RIGHT, anchor=N, padx=100, pady=60)
        
        # 뉴스
        self.news = News(self.bottomFrame)
        self.news.pack(side=LEFT, anchor=W, padx=100, pady=60)
        
        # 날씨
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=N, padx=100, pady=60)
        '''
        # 캘린더
        self.calender = Calendar(self.bottomFrame)
        self.calender.pack(side = RIGHT, anchor=E, padx=100, pady=60)
        '''
    def go_fullscreen(self, event=None):
        self.state = not self.state
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':
    w = FullscreenWindow()
    w.tk.mainloop()
