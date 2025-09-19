#1. Скроллбар для элементов. 
#2. Левая панель с информацией
#3. Редактирование
#4. Таблица MAC-адресов

import tkinter as tk
from tkinter import ttk
from tkinter import Frame, Tk, BOTTOM
import mysql.connector
from tkinter import messagebox
from PIL import ImageTk, Image

switches = ["switch_184"] #будет заменено
switches_characteristics = ["switch_184_characteristics"] #будет заменено

switch = switches[0] #будет заменено
switch_characteristics = switches_characteristics[0] #будет заменен

connection = mysql.connector.connect(
host="",
user="",
passwd="",
database="")
cursor = connection.cursor() #ставим курсор


def rundom_switch():
    cursor.execute(f"SELECT * FROM {switch}")
    main_data = cursor.fetchall()
    cursor.execute(f"SELECT * FROM {switch_characteristics}")
    characteristics_data = cursor.fetchall()

    root = tk.Tk()
    root.title(f"Панель управления коммутатором {characteristics_data[0][0]}")
    root.geometry("1400x440")
    root.resizable(True, True)    

    ports = 52 #сюда пробрасывать переменную по числу портов
    heading = ['№ ', 'Тип порта', 'Описание', 'Настройки']
    
    mainframe = tk.Frame(root)
    portframe = tk.Frame(root)
    mainframe.pack(side="left", fill="both", expand=True)
    portframe.pack(side="right", fill="both", expand=True)
    
    maincanvas = tk.Canvas(mainframe) #левое окно width=300, height=200
    portcanvas = tk.Canvas(portframe, width=1000) #правое окно (окно с портами) width=1000, height=400
    maincanvas.pack(side="left", fill="both", expand=True)
    portcanvas.pack(side="left", fill="both", expand=True)

    #создаем область прокрутки
    main_scrollable_frame = tk.Frame(maincanvas)
    maincanvas.create_window((0, 0), window=main_scrollable_frame, anchor='nw')
    
    port_scrollable_frame = tk.Frame(portcanvas)
    portcanvas.create_window((0, 0), window=port_scrollable_frame, anchor='nw')

    style = ttk.Style()
    style.theme_use("classic")
    style.configure("Main.Treeview", background="white", foreground="black", font=("Times New Roman", 12), rowheight=40)
    style.configure('Heading', background="black", foreground="white", font=("Times New Roman", 12))
    
    tree = ttk.Treeview(port_scrollable_frame, show='headings', style="Main.Treeview")
    tree["columns"] = ("col0", "col1", "col2", "col3")

    heading_range = range(len(heading))
    
    #заголовки
    for row, head in zip(heading_range, heading):
        tree.heading(f"col{row}", text=head)
        if row == 0:
            tree.column("col0", width=50) 
        elif row == 1:
            tree.column("col1", width=80) 
        elif row == 2:
            tree.column("col2", width=400) 
        elif row == 3:
            tree.column("col3", width=800)
   
    #порты
    for i in range(ports): #тут число портов
        count = len(main_data)
        if i < count:
            tree.insert("", tk.END, values=(main_data[i]))
        else:
            tree.insert("", tk.END, values=())
    tree.pack()

    #обновляются данные кнопки. тут должно быть занесение в таблицы настроек коммутатора определнных данных
    def update_location(event):
        selected_value = options.get()
        button.config(text=selected_value)
        
        cursor = connection.cursor() #ставим курсор
        command = f"UPDATE {switch}_characteristics SET Location = '{selected_value}'" #команда
        cursor.execute(command) #исполняем команду
        connection.commit()


    values = ["Отключен", "Центральная, 20А", "Береговая, 16"] #сюда выгружаются данные из таблицы с адресами
    options = ttk.Combobox(mainframe, values=values, width=18, state='readonly')
    options.place(x = 145, y = 105)
    options.bind("<<ComboboxSelected>>", update_location)

    label0 = tk.Label(mainframe, text="Основное:", font="TimesNewRoman 12").place(x=100, y=5)
    label1 = tk.Label(mainframe, text="IP-адрес:", font="TimesNewRoman 10").place(x=5, y=30)
    label2 = tk.Label(mainframe, text="Логин:", font="TimesNewRoman 10").place(x=5, y=55)
    label3 = tk.Label(mainframe, text="Пароль:", font="TimesNewRoman 10").place(x=5, y=80)
    label4 = tk.Label(mainframe, text="Расположение:", font="TimesNewRoman 10").place(x=5, y=105)
    label5 = tk.Label(mainframe, text="Марка:", font="TimesNewRoman 10").place(x=5, y=130)
    label6 = tk.Label(mainframe, text="Прошивка:", font="TimesNewRoman 10").place(x=5, y=155)
    label7 = tk.Label(mainframe, text="Железо:", font="TimesNewRoman 10").place(x=5, y=180)

    entry1 = tk.Entry(mainframe,width=18).place(x=120, y=30)
    entry2 = tk.Entry(mainframe,width=18).place(x=120, y=55)
    entry3 = tk.Entry(mainframe,width=18).place(x=120, y=80)
    button = tk.Button(mainframe, text="", command=lambda: None, width=18) #прописать функцию выбора локации
    button.place(x=120, y=105)
    entry5 = tk.Entry(mainframe,width=18).place(x=120, y=130)
    entry6 = tk.Entry(mainframe,width=18).place(x=120, y=155)
    entry7 = tk.Entry(mainframe,width=18).place(x=120, y=180)

    scrollbar_verticall = tk.Scrollbar(portframe, orient="vertical", command=tree.yview)
    scrollbar_verticall.pack(side="left", fill="y")
    tree.configure(yscrollcommand=scrollbar_verticall.set)
   
    scrollbar_horizontal = tk.Scrollbar(port_scrollable_frame, orient="horizontal", command=portcanvas.xview)
    scrollbar_horizontal.pack(side="bottom", fill="x")
    tree.configure(xscrollcommand=scrollbar_horizontal.set)
        
    root.mainloop()
  
rundom_switch()
