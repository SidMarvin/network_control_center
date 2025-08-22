import mysql.connector
import hashlib
import threading
import pyperclip
import keyboard
from tkinter import *
from tkinter import messagebox
import tkinter as tk

#функция копирования, нужно сделать поле откуда копировать entry глобальным
def copy_text():
    text_to_copy = entry.get()
    pyperclip.copy(text_to_copy)

#ожидание сочетания клавишь
def expectation():
    while True:
        keyboard.wait("ctrl+c")
        copy_text()

#сетевые настройки
def network_properties():
    window = Tk()
    window.title("Настройки подключения")
    window.geometry("500x300")
    window.resizable(False, False)
    label1 = Label(window, text = "IP-адрес сервера", font="Garamond 12")
    label1.place(x=10, y=10)
    label2 = Label(window, text = "Имя базы данных", font="Garamond 12")
    label2.place(x=10, y=80)
    host = Entry(window, width=20)
    host.place(x=150, y=10)
    database = Entry(window, width=20)
    database.place(x=150, y=80)
    #модуль shelve для созданий кэш-файла для сохранения учетных данных

#аунтефикация
def authentication(user, password):
    user = user.get()
    password = password.get()
    
    #данные (логин и пароль) для подключения нужно загружать из зашифрованного кэш-файла
    #хост и имя базы загружаются из настроек
    
    #параметры подключения к БД
    connection = mysql.connector.connect(
      host="",
      user="",
      passwd="",
      database="")
    
    #курсор
    cursor = connection.cursor()
    
    #запрос
    cursor.execute("SELECT * FROM logpass")
    results = cursor.fetchall()
    
    for row in results:
        list(row)
        authentication_string = row[1] + row[2]
        loginpassword_string = user+password
        hash_object_1 = hashlib.sha256(user.encode())
        hex_dig_1 = hash_object_1.hexdigest()
        hash_object_2 = hashlib.sha256(password.encode())
        hex_dig_2 = hash_object_2.hexdigest()
        hash_string = str(hex_dig_1 + hex_dig_2)
        
        if authentication_string == hash_string:
            messagebox.showinfo("Вход выполнен","Вы вошли в систему")
            cursor.close()
            #connection.close()
            root.destroy()
            main_window()
            break
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
            connection.close()
            break
            
#основное окно
def main_window():
    window = Tk()
    window.title("Центр управления сетью")
    window.geometry("800x650")
    window.resizable(False, False)
    
    img = PhotoImage(file="logo1.png")
    label_main = Label(window, image=img)
    label_main.image_ref = img
    label_main.grid(row=0, column=0)
    
    label_1 = Label(window, text="Расположения", font=("Times New Roman", 15))
    label_1.place(x=50, y=390) 
    label_2 = Label(window, text="Узлы сети", font=("Times New Roman", 15))
    label_2.place(x=250, y=390) 
    label_3 = Label(window, text="Документация", font=("Times New Roman", 15))
    label_3.place(x=450, y=390) 
    label_4 = Label(window, text="Служебное", font=("Times New Roman", 15))
    label_4.place(x=650, y=390) 

    button_1 = Button(window, text="Многоквартирные дома", width=20, command=lambda: None)
    button_1.place(x=50, y=430)
    button_2 = Button(window, text="Серверные", width=20, command=lambda: None)
    button_2.place(x=50, y=455)
    button_3 = Button(window, text="Локальные сети", width=20, command=lambda: None)
    button_3.place(x=50, y=480)
    button_4 = Button(window, text="Коттеджи", width=20, command=lambda: None)
    button_4.place(x=50, y=505)

    button_5 = Button(window, text="Коммутаторы", width=20, command=lambda: None)
    button_5.place(x=250, y=430)
    button_6 = Button(window, text="Серверы", width=20, command=lambda: None)
    button_6.place(x=250, y=455)
    button_7 = Button(window, text="Оптические кроссы", width=20, command=lambda: None)
    button_7.place(x=250, y=480)
    button_8 = Button(window, text="Модемы", width=20, command=lambda: None)
    button_8.place(x=250, y=505)
    
    button_9 = Button(window, text="IP-план", width=20, command=lambda: None)
    button_9.place(x=450, y=430)
    button_10 = Button(window, text="VLAN", width=20, command=lambda: None)
    button_10.place(x=450, y=455)
    button_11 = Button(window, text="Каналы связи", width=20, command=lambda: None)
    button_11.place(x=450, y=480)
    button_12 = Button(window, text="Платежные системы", width=20, command=lambda: None)
    button_12.place(x=450, y=505)
    
    button_13 = Button(window, text="Статистика", width=20, command=lambda: None)
    button_13.place(x=650, y=430)
    button_14 = Button(window, text="Служебная информация", width=20, command=lambda: None)
    button_14.place(x=650, y=455)
    button_15 = Button(window, text="Свободные IP", width=20, command=lambda: None)
    button_15.place(x=650, y=480)
    button_16 = Button(window, text="", width=20, command=lambda: None)
    button_16.place(x=650, y=505)

    label_5 = Label(window, text = "Поиск адреса", font=("Times New Roman", 12))
    label_5.place(x=50, y=550) 
    
    label_6 = Label(window, text = "Поиск узла", font=("Times New Roman", 12))
    label_6.place(x=250, y=550) 
    
    entry_1 = Entry(window,width=25)
    entry_1.place(x=50, y=580) 
    entry_2 = Entry(window,width=25)
    entry_2.place(x=250, y=580) 

"""
    but0 = Button(window, text="Выход", command=lambda: exit())
    but0.place(x=700, y=580)
"""
    
#начальное окно
def start_window():
    global root
    root = Tk()
    root.title("Центр управления сетью")
    root.geometry("800x650")
    root.resizable(False, False)
    img = PhotoImage(file="logo.png")
    label = Label(root, image=img)
    label.image_ref = img
    label.grid(row=0, column=0)
    text = Label(root, text="Пожалуйста, авторизуйтесь в системе:", font=("Times New Roman", 17))
    text.place(x=250, y=390)
    user = Entry(root, width=40)
    user.place(x=250, y=430)
    password = Entry(root, show="*", width=40)
    password.place(x=250, y=450)
    button_1 = Button(root, text="Войти", command=lambda: authentication(user, password))
    button_1.place(x=340, y=475)
    button_2 = Button(root, text="Открыть свойство подключения", command=lambda: network_properties())
    button_2.place(x=600, y=600)

    root.mainloop()

#тут будут функции узлов и расположений





thread1 = threading.Thread(target=start_window)
thread2 = threading.Thread(target=expectation)

thread1.start()
thread2.start()

