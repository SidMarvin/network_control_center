#1. Скроллбар для элементов
#2. Левая панель с информацией
#3. Редактирование
#4. Выбор адреса

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
    root.geometry("1400x450")
    root.resizable(False, False)    

    ports = 52 #сюда пробрасывать переменную по числу портов
    heading = ['№ ', 'Тип порта', 'Описание', 'Настройки']

    style = ttk.Style()
    style.theme_use("classic")
    style.configure("Main.Treeview", background="white", foreground="black", font=("Times New Roman", 12), rowheight=40)
    style.configure('Heading', background="black", foreground="white", font=("Times New Roman", 12))
    
    tree = ttk.Treeview(root, show='headings', style="Main.Treeview")
    tree["columns"] = ("col0", "col1", "col2", "col3")

    heading_range = range(len(heading)) #тут заменить на len(heading)
    
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
    
    tree.place(x=250, y=1)

    vsb_y = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb_y.set)
    vsb_y.place(x=1380, y=1, height=410)
    
    vsb_x = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=vsb_x.set)
    vsb_x.place(x=250, y=411, width=1125)
    
    root.mainloop()

    


  
    
rundom_switch()
