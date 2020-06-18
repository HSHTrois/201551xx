# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 13:53:40 2020

@author: hshyu
"""

from tkinter import *
import tkinter.ttk
import pickle
import os
import time

values=['내과', '외과'] 
button_list = ["저장", '지우기']
waitlist_dic = {}
# savefile_root = "./data/waitlist.p"
savefile_root = r"\\192.168.1.139\pi\data\waitlist.p"
tk=Tk()
tk.title("wait list input")
tk.geometry("400x400")
tk.resizable(False, False)

# 이름 text
nlabel = Label(tk, width = 10,text = '이름')
nlabel.grid(row = 0,column = 0)

# 병과 text
jlabel = Label(tk, width = 10, text = '병과')
jlabel.grid(row = 1,column = 0)

# 이름 입력
name_input = Entry(tk)
name_input.grid(row = 0,column = 1)

# 병과 선택
department = tkinter.ttk.Combobox(tk, height=15, values=values)
department.grid(row =1,column = 1)
department.set("병과 선택")

internal_text = Label(tk, text="내과")
internal_text.grid(row=3, column=0)
surgery_listbox = Label(tk, text="외과")
surgery_listbox.grid(row=3, column=1)

internal_listbox = Listbox(tk)
internal_listbox.grid(row=4, column=0)
surgery_listbox = Listbox(tk)
surgery_listbox.grid(row=4, column=1)

# 파일의 내용을 읽어서 사용할 딕셔너리에 저장 후 닫아줌.
if os.path.exists(savefile_root):
    onfile = open(savefile_root,'rb')
    waitlist_dic = pickle.load(onfile)
    onfile.close()

# 리스트 박스에 데이터 추가
    
def listbox_update():
    global waitlist_dic
    surgery_listbox.delete(0,'end')
    internal_listbox.delete(0,'end')
    
    for names in waitlist_dic:
        if waitlist_dic[names] == "외과":
            surgery_listbox.insert(END, names)   # 끝에 삽입, listbox.insert(len(listbox), items[names])
        else:
            internal_listbox.insert(END, names)   # 끝에 삽입, listbox.insert(len(listbox), items[names])

def click(key):
    global waitlist_dic
    if key == "저장":
        # 정보 미 입력시
        if name_input.get() == None or department.get() == '병과 선택':
            messagebox.showinfo("정보 오류", "정보 입력을 정확하게 하세요.")
            print("정보를 다시 입력하세요.")
        # waitlist_dic에 새로운 정보 입력
        elif name_input.get() not in waitlist_dic.keys(): 
            waitlist_dic[name_input.get()] = department.get() # 새로운 키와 값을 딕셔너리에 저장
            # 파일을 쓰기 모드로 열기
            file = open(savefile_root, 'wb')
            pickle.dump(waitlist_dic, file) # 딕셔너리가 저장하던 키와 값을 모두 파일에 작성
            file.close() # 파일을 닫음과 동시에 저장됨
            listbox_update()
        else : #이전에 존재하던 이름이라면 
            messagebox.showinfo("중복 등록", "중복 등록입니다.")
            print("중복 등록입니다.")

    elif key == "지우기":
        # 데이터 없을 때
        if not os.path.exists(savefile_root):
            messagebox.showinfo("데이터 없음", "데이터가 없습니다.입력하세요.")
            print("데이터가 없습니다.입력하세요.")
        # waitlist_dic에 해당 key와 value가 존재할 때
        elif name_input.get() in waitlist_dic.keys() and department.get() == waitlist_dic[name_input.get()]:
            del waitlist_dic[name_input.get()]
            os.remove(savefile_root)
            print("지우는중...")
            #time.sleep(1)
            file = open(savefile_root, 'wb')
            pickle.dump(waitlist_dic, file) # 딕셔너리가 저장하던 키와 값을 모두 파일에 작성
            file.close() # 파일을 닫음과 동시에 저장됨
            listbox_update()
            print('remove name!')
        # 정보 기입 잘못됬을때
        else:
            messagebox.showinfo("정보 오류", "정보 입력을 정확하게 하세요.")
            print("정보를 다시 입력하세요.")

num = 0
for i in button_list:
    def process(t = i):
        click(t)
    Button(tk, text = i, command = process).grid(row = 2, column = num)
    num += 1

    
for names in waitlist_dic:
    if waitlist_dic[names] == values[1]:
        surgery_listbox.insert(END, names)   # 끝에 삽입, listbox.insert(len(listbox), items[names])
    else:
        internal_listbox.insert(END, names)   # 끝에 삽입, listbox.insert(len(listbox), items[names])
        

tk.mainloop()