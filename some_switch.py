#1. Скроллбар для элементов. 
#дело в цифрах. высота в канвасе позволяет прокручивать фрейм только на какое-то число клеток
#2. Левая панель с информацией
#3. Редактирование
#4. Выбор адреса
#5. Таблица MAC-адресов

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
host="192.168.58.240",
user="admin",
passwd="MiloRd12",
database="nnc_db")
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

    #начало###################################################
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


    """scrollbar_vertical = tk.Scrollbar(portframe, orient="vertical") #это вертикальная полоса прокрутки, привязывается к фрейму
    scrollbar_vertical.pack(side="right", fill="y") #размещение
    scrollbar_vertical.config(command=portcanvas.yview) #конфигурация полосы прокрутки, какой канвас прокручивать
    portcanvas.config(yscrollcommand=scrollbar_vertical.set)

    scrollbar_horizontal = tk.Scrollbar(port_scrollable_frame, orient="horizontal") #это горизонтальная полоса прокрутки, привязывается к фрейму
    scrollbar_horizontal.pack(side="bottom", fill="x")
    scrollbar_horizontal.config(command=portcanvas.xview)
    portcanvas.config(xscrollcommand=scrollbar_horizontal.set)"""
    #конец###################################################

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
            tree.column("col0", width=50) #
        elif row == 1:
            tree.column("col1", width=80) #80
        elif row == 2:
            tree.column("col2", width=400) #400
        elif row == 3:
            tree.column("col3", width=800) #800
   
    #порты
    for i in range(ports): #тут число портов
        count = len(main_data)
        if i < count:
            tree.insert("", tk.END, values=(main_data[i]))
        else:
            tree.insert("", tk.END, values=())
    tree.pack()


    scrollbar_verticall = tk.Scrollbar(portframe, orient="vertical", command=tree.yview)
    scrollbar_verticall.pack(side="left", fill="y")
    tree.configure(yscrollcommand=scrollbar_verticall.set)
   
    scrollbar_horizontal = tk.Scrollbar(port_scrollable_frame, orient="horizontal", command=portcanvas.xview)
    scrollbar_horizontal.pack(side="bottom", fill="x")
    tree.configure(xscrollcommand=scrollbar_horizontal.set)
    
    ###изменение###########################################
    #port_scrollable_frame.update_idletasks() #обновляем данные по канвас
    #portcanvas.config(scrollregion=portcanvas.bbox("all"))
    ###изменение###########################################
    
    root.mainloop()
  
rundom_switch()
