from __future__ import print_function
from contextlib import contextmanager
from tkinter import *

from urllib.parse import quote_plus
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver

from urllib.request import urlopen, Request
import urllib
import time

from PIL import Image, ImageTk

import feedparser
# from win32api import GetSystemMetrics
import sys

import pickle
import os
import random

date_format = "%Y년 %m월 %d일"
xlarge_text_size = 45
large_text_size = 35
medium_text_size = 25
small_text_size = 15
locale = 'ko_kr' 
setfont = '맑은 고딕'
DayOfWeek = ['월', '화', '수', '목', '금', '토', '일']
AMPM = {'AM':'오전', 'PM':'오후'}
weather_locale = '춘천시 옥천동'
hour_1 = 3600000 # 1시간
minute_10 = 600000 # 10분
minute_1 = 60000 # 1분

patient_kind = ['확진환자', '완치(격리해제)', '치료중(격리 중)', '사망']
patient_num = [None] * 4
patient_increase = [None] * 4

file_path = "./Image/"
file_list = os.listdir(file_path)
random.shuffle(file_list)
tkimg = [None for i in range(len(file_list))]
im_num = 0

internaltitle = '내과 대기'
surgerytitle = '외과 대기'
waitlist_dic = {}
savefile_root = r"\\192.168.1.139\pi\data\waitlist.p"

class Clock(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='black')
        # 시간
        self.time1 = ''
        self.timeLbl = Label(self, font=(setfont, large_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=NW)
        
        # 나머지 요일
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=(setfont, medium_text_size), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=NW)
        '''
        # 시계 밑에 워터마크
        self.watermark = '\n캡스톤 김휘진 양상열 황승현'
        self.watermarkLbl = Label(self, text=self.watermark, font=(setfont, small_text_size, 'bold'), fg="white", bg="black")
        self.watermarkLbl.pack(side=TOP, anchor=E)
        '''
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
        self.weatherLbl1.pack(side=TOP, anchor=NW)
        # 온도
        self.weatherLbl2 = Label(self.weatherContainer, text = self.temperature, font=(setfont, large_text_size), fg = "white", bg = "black")
        self.weatherLbl2.pack(side=TOP, anchor=NW)
        
        # 상세정보
        self.weatherLbl3 = Label(self.weatherContainer, text = self.weatherinfo, font=(setfont, small_text_size), fg = "white", bg = "black")
        self.weatherLbl3.pack(side=TOP, anchor=W)
        
        # 날씨 테스트용
        print('============================')
        print('weather update time' + time.strftime(' %I:%M'))
        print(self.temperature)
        # print(self.weatherinfo)
        print('============================')
        
        # 1시간마다 업데이트
        self.after(hour_1, self.parsing)

class Corona(Frame):
     def __init__(self, parent):
        Frame.__init__(self, parent, bg='black')
        self.coronaContainer = Frame(self, bg="black")
        self.coronaContainer.pack(side=TOP, anchor=NE)
        self.parsing()
    
     def parsing(self):
        
        # tk 새로고침 위한 destroy()
        for widget in self.coronaContainer.winfo_children():
            widget.destroy()
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('lang=ko_KR')
        driver = webdriver.Chrome(r'C:\Users\hshyu\ChromeWebDriver\chromedriver.exe')
        
        url = 'http://ncov.mohw.go.kr/'
        
        driver.get(url)

        html = driver.page_source
        soup = BeautifulSoup(html)
        
        driver.close()
        
        span_num = soup.select('span.num')
        span_before = soup.select('span.before')
        
        # 총 수
        i = 0
        for num in span_num:
            patient_num[i] = num.get_text()
            print(patient_num[i])
            i += 1
            if i > 3:
                break
        # 증가 수
        i = 0
        for num in span_before:
            patient_increase[i] = num.get_text()
            i += 1
            if i > 3:
                break
        

        # 코로나 제목
        self.coronaLbl0 = Label(self.coronaContainer, text = "코로나-19",font=(setfont, xlarge_text_size, 'bold'), fg = "white", bg = "black")
        self.coronaLbl0.pack()
        
        for i in range(len(patient_kind)):
            self.coronaLbl1 = Label(self.coronaContainer, text=patient_kind[i], font=(setfont, medium_text_size, 'bold'), fg='white', bg = "black")
            self.coronaLbl1.pack()
            self.coronaLbl2 = Label(self.coronaContainer, text=patient_num[i], font=(setfont, medium_text_size), fg='white', bg = "black")
            self.coronaLbl2.pack()
            self.coronaLbl3 = Label(self.coronaContainer, text=patient_increase[i], font=(setfont, small_text_size), fg='white', bg = "black")
            self.coronaLbl3.pack()
        
        # 1시간마다 업데이트
        self.after(hour_1, self.parsing)
        
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
            
        # 1시간마다 업데이트
        self.after(hour_1, self.get_headlines)

class Ad_viewer(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        img_list = os.listdir(file_path)
        
        baseheight = 700
        basewidth = 1080
        
        for i in range(len(file_list)):
            img = Image.open(file_path + file_list[i])
            # 세로 700 기준
            hpercent = (baseheight / float(img.size[1]))
            wsize = int((float(img.size[0])*float(hpercent)))

            # 만약 변환 가로가 1080이 넘는다면
            if wsize > 1080:
                wpercent = (basewidth / float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
    
                img = img.resize((basewidth,hsize), Image.ANTIALIAS)
            else:
                img = img.resize((wsize,baseheight), Image.ANTIALIAS)
                
            tkimg[i] = ImageTk.PhotoImage(img)
        

        self.adLbl = Label(self, image=tkimg[0], borderwidth=0, highlightthickness=0)
        # self.adLbl.img = tkimg
        self.adLbl.pack(anchor = CENTER)
        self.update_image()
        
    def update_image(self):
        global tkimg
        global im_num
        if im_num == len(tkimg):
            im_num = 0
        # tkimg[num] = ImageTk.PhotoImage(Image.open(file_path + file_list[im_num]))
        
        self.adLbl.config(image = tkimg[im_num])
        self.adLbl.after(15000, self.update_image)
        print("Updated")
        print(im_num)
        im_num += 1

class WaitLabel(Frame):
    def __init__(self, parent, title):
        Frame.__init__(self, parent)
        print("title : ", title)
        self.config(bg='black')
        self.morbidLbl = Label(self, text=title, font=(setfont, xlarge_text_size, 'bold'), fg="white", bg="black")
        self.morbidLbl.pack(side=TOP, anchor=W)
        self.morbidContainer = Frame(self, bg="black")
        self.morbidContainer.pack(side=LEFT)

class WaitList(Frame):
    def __init__(self, parent, title):
        Frame.__init__(self, parent)
        self.config(bg='black')
        self.WaitListContainer = Frame(self, bg="black")
        self.WaitListContainer.pack(side=TOP)
        self.title_a = title
        self.update()
        
    def update(self):
        global waitlist_dic
        
        # tk 새로고침 위한 destroy()
        print("================waitlist children()==============\n", self.WaitListContainer.winfo_children())
        for widget in self.WaitListContainer.winfo_children():
            print("waitlist destroy")
            widget.destroy()
        
        if os.path.exists(savefile_root):
            onfile = open(savefile_root,'rb')
            waitlist_dic = pickle.load(onfile)
            onfile.close()

        num = 1
        for names, value in waitlist_dic.items():
            # 내과
            if self.title_a == internaltitle:
                if value == '내과':
                    num_and_name = str(num) + ". " + names
                    self.wait_name = Label(self.WaitListContainer, text=num_and_name, font=(setfont, large_text_size), fg="white", bg="black")
                    self.wait_name.pack(side=TOP, anchor=W)
                    num += 1
            # 외과
            else :
                if value == '외과':
                    num_and_name = str(num) + ". " + names
                    self.wait_name = Label(self.WaitListContainer, text=num_and_name, font=(setfont, large_text_size), fg="white", bg="black")
                    self.wait_name.pack(side=TOP, anchor=W)
                    num += 1
        # 2초마다 업데이트
        self.after(2000, self.update)
        print("update")

class FullscreenWindow:
    def __init__(self):
        self.tk = Tk()
        # self.tk = Toplevel()
        self.tk.configure(background='black')

        self.frame = Frame(self.tk, background = 'black')
        self.frame.pack(fill=BOTH, expand=YES)
        
        # 전체화면
        self.state = False # 전체화면 우선 False로 설정 후 아래 실행
        self.tk.attributes("-fullscreen", True) # 일단 자동으로 바로 전체화면 뜨게함
        self.tk.bind("<Return>", self.go_fullscreen) # 엔터 누르면 전체화면
        self.tk.bind("<Escape>", self.end_fullscreen) # esc 종료
        
        # top
        # 시계
        self.clock = Clock(self.frame)
        self.clock.place(x=10, y=10)

        # 날씨
        self.weather = Weather(self.frame)
        self.weather.place(x=10, y=170)
        
        # 뉴스
        self.news = News(self.frame)
        self.news.place(x=10, y=380)
        
        # 코로나
        self.corona = Corona(self.frame)
        self.corona.place(x=840, y=10)
        
        # 네이버 실검
        # self.naver = Naver_RT_search_word(self.frame)
        # self.naver.place(x=820, y=10)
        
        # middle
        # 광고 사진
        self.adview = Ad_viewer(self.frame)
        self.adview.place(y=990, relx=0.5, anchor=CENTER)
        
        # bottom
        # 병과
        self.internal_title = WaitLabel(self.frame, internaltitle)
        self.internal_title.place(x=150,y=1350)
        
        self.surgery_title = WaitLabel(self.frame, surgerytitle)
        self.surgery_title.place(x=690,y=1350)
                
        # 대기자 리스트
        self.internal_wait = WaitList(self.frame, internaltitle) 
        self.internal_wait.place(x=160,y=1450)

        self.surgery_wait = WaitList(self.frame, surgerytitle)
        self.surgery_wait.place(x=700,y=1450)
        
        self.disinfec = Label(self.frame,text="↓손소독제↓", font=(setfont, medium_text_size, 'bold'), fg="white", bg="black")
        self.disinfec.place(y=2000, relx=0.5, anchor=CENTER)
        
    def go_fullscreen(self, event=None):
        self.state = not self.state
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':
    sys.setrecursionlimit(2000)
    w = FullscreenWindow()
    w.tk.mainloop()

