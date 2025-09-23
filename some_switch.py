

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
    root.resizable(False, False)

    canvas = tk.Canvas(root)
    canvas.pack()

    mainframe = tk.Frame(canvas, width=350, height=400)
    mainframe.pack(side="left")

    portframe = tk.Frame(canvas, width=1050, height=400)
    portframe.pack(side="right")

    ports = 52 #сюда пробрасывать переменную по числу портов
    heading = ['№ ', 'Тип порта', 'Описание', 'Настройки']

    style = ttk.Style()
    style.theme_use("classic")
    style.configure("Main.Treeview", background="white", foreground="black", font=("Times New Roman", 12), rowheight=40)
    style.configure('Heading', background="black", foreground="white", font=("Times New Roman", 12))
    
    tree = ttk.Treeview(portframe, show='headings', style="Main.Treeview")
    tree["columns"] = ("col0", "col1", "col2", "col3")

    heading_range = range(len(heading))

    #заголовки
    for row, head in zip(heading_range, heading):
        tree.heading(f"col{row}", text=head)

    tree.column("col0", width=50) 
    tree.column("col1", width=150) 
    tree.column("col2", width=300)
    tree.column("col3", width=1500)

    #порты
    for i in range(ports): #тут число портов
        count = len(main_data)
        if i < count:
            tree.insert("", tk.END, values=(main_data[i]))
        else:
            tree.insert("", tk.END, values=())

    #обновляются данные кнопки. тут должно быть занесение в таблицы настроек коммутатора определнных данных
    def update_location(event):
        selected_value = options.get()
        button.config(text=selected_value)
        
        cursor = connection.cursor() #ставим курсор
        command = f"UPDATE {switch}_characteristics SET Location = '{selected_value}'" #команда
        cursor.execute(command) #исполняем команду
        connection.commit()

    def edit_button():
        try:
            editing_window = tk.Tk()
            editing_window.title("Окно редактирования")
            editing_window.geometry("550x250")

            def save_button():  
                value1 = entry1.get()
                value2 = entry2.get()
                value3 = entry3.get()

                cursor = connection.cursor() #ставим курсор
                command = f"UPDATE {switch} SET Type = '{value1}', Description = '{value2}', Port_settings = '{value3}' WHERE Number = {values[0]}" #команда
                cursor.execute(command) #исполняем команду
                connection.commit()
                
                selected_item_id = tree.selection()[0]
                tree.item(selected_item_id, values=(values[0], value1, value2, value3)) #данные для обновления

            selected_item = tree.selection()
            
            if selected_item:
                values = tree.item(selected_item)["values"]

            for row, head in zip(range(0, len(heading)), heading):
                label = tk.Label(editing_window, text=head, font=("Times New Roman", 12))
                label.grid(row=row, column=0)
            
            id = tk.Label(editing_window, text = values[0], font=("Times New Roman", 12), relief="groove", width=17, height=1)
            id.grid(row=0, column=1)
            
            #оптимизировать 2
            entry1 = tk.Entry(editing_window, font=("Times New Roman", 12), width=50)
            entry1.grid(row=1, column=1)
            entry1.insert(0, values[1])
            entry2 = tk.Entry(editing_window, font=("Times New Roman", 12), width=50)
            entry2.grid(row=2, column=1)
            entry2.insert(0, values[2])
            entry3 = tk.Entry(editing_window, font=("Times New Roman", 12), width=50)
            entry3.grid(row=3, column=1)
            entry3.insert(0, values[3])

            save_button = tk.Button(editing_window, text = "Сохранить", command= save_button, font=("Times New Roman", 12))
            save_button.place(x=10, y=200)
            close_button = tk.Button(editing_window, text = "Выход", command=lambda: editing_window.destroy(), font=("Times New Roman", 12))
            close_button.place(x=100, y=200)
            
            editing_window.mainloop()
        except:
            messagebox.showerror("Ошибка", "Выберите строчку")
            editing_window.destroy()

    values = ["Отключен"] #сюда выгружаются данные из таблицы с адресами
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

    button1 = tk.Button(mainframe, text="Открыть в браузере", command=lambda: None, width=18, font="TimesNewRoman 10")
    button1.place(x=5, y=205)
    button2 = tk.Button(mainframe, text="Редактировать", command=lambda: edit_button(), width=18, font="TimesNewRoman 10")
    button2.place(x=180, y=205)
    button3 = tk.Button(mainframe, text="Таблица MAC-адресов", command=lambda: None, width=18, font="TimesNewRoman 10")
    button3.place(x=5, y=250)
    button4 = tk.Button(mainframe, text="Настройки коммутатора", command=lambda: None, width=18, font="TimesNewRoman 10")
    button4.place(x=180, y=250)
    button5 = tk.Button(mainframe, text="Сохр", command=lambda: None,width=4, height=2, font="TimesNewRoman 10")
    button5.place(x=250, y=150)

    scrollbar_vertical = tk.Scrollbar(portframe, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_vertical.set)
    scrollbar_vertical.pack(side="right", fill="y")

    scrollbar_horizontal = tk.Scrollbar(portframe, orient='horizontal', command=tree.xview)
    tree.configure(xscrollcommand=scrollbar_horizontal.set)
    scrollbar_horizontal.pack(side='bottom', fill='x')

    tree.pack(side='top', fill='both', expand=True)
    root.mainloop()
    
rundom_switch()   
