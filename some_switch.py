"""
Не забыть:
1. Заменить список домов для выбора локации. Нужно получать общий список именований из трех таблиц расположений: многоквартирные дома, серверные, локальные сети
2. Написать функцию. Скорее всего это будет функция глобального поиска по всем расположениям, но аргументом будет текст кнопки.
3. Оптимизировать. Идея оптимизации состоит в следующем: создать списки для с названиями для лейблов, и в ициклах создавать их
"""

import tkinter as tk
from tkinter import ttk
from tkinter import Frame, Tk, BOTTOM
import mysql.connector
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import *
import webbrowser

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

    def save_settings_button():
        value1 = entry1.get()
        value2 = entry2.get()
        value3 = entry3.get()
        value5 = entry5.get()
        value6 = entry6.get()
        value7 = entry7.get()
        
        cursor = connection.cursor() #ставим курсор
        command = f"UPDATE {switch}_characteristics SET IP_addr = '{value1}', Login = '{value2}', Password = '{value3}', Brand = '{value5}', Firmware = '{value6}', Hardware = '{value7}'" #команда
        cursor.execute(command) #исполняем команду
        connection.commit()

    #обновляются данные кнопки. тут должно быть занесение в таблицы настроек коммутатора определнных данных
    def update_location(event):
        selected_value = options.get()
        button.config(text=selected_value)
        
        cursor = connection.cursor() #ставим курсор
        command = f"UPDATE {switch}_characteristics SET Location = '{selected_value}'" #команда
        cursor.execute(command) #исполняем команду
        connection.commit()
        
    #кнопка настроек коммутатора
    def setting_switch_button():
        cursor.execute(f"SELECT setting, value FROM {switch}_setting")
        settings = cursor.fetchall()
        cursor.execute(f"SELECT COUNT(*) FROM {switch}_setting")
        count_table = cursor.fetchall()
        count_table = count_table[0][0]
        #кнопка для редактирования настроек
        def setting_edit_button():
            cursor.execute(f"SELECT * FROM {switch}_setting")
            settings = cursor.fetchall()
            try:
                editing_setting_window = tk.Tk()
                editing_setting_window.title("Окно ввода настроек")
                editing_setting_window.geometry("600x300")
                editing_setting_window.resizable(False, False)
                
                #кнопка сохранить, данную функцию необходимо исправить
                def save_button():  
                    value1 = entry1.get()
                    value2 = entry2.get()
                    cursor = connection.cursor() #ставим курсор
                    command = f"UPDATE {switch}_setting SET setting = '{value1}', value = '{value2}' WHERE ID = {ID_str}" #команда
                    cursor.execute(command) #исполняем команду
                    connection.commit()

                    selected_item_id = setting_table.selection()[0]
                    setting_table.item(selected_item_id, values=(value1, value2)) #данные для обновления
                    
                selected_port = setting_table.selection()

                if selected_port:
                    values = setting_table.item(selected_port)["values"]
                    
                hex_id = selected_port[0][1:]
                ID_str = int(hex_id, 16)
                    
                label1 = tk.Label(editing_setting_window, text = "Настройка", font=("Times New Roman", 12))
                label1.grid(row=0, column=0)
                label2 = tk.Label(editing_setting_window, text = "Значение", font=("Times New Roman", 12))
                label2.grid(row=1, column=0)
                entry1 = tk.Entry(editing_setting_window, font=("Times New Roman", 12))
                entry1.grid(row=0, column=1)
                entry1.insert(0, values[0])
                entry2 = tk.Entry(editing_setting_window, font=("Times New Roman", 12))
                entry2.grid(row=1, column=1)
                entry2.insert(0, values[1])


                save_button = tk.Button(editing_setting_window, text = "Сохранить", command= save_button, font=("Times New Roman", 12))
                save_button.place(x=10, y=230)
                close_button = tk.Button(editing_setting_window, text = "Выход", command=lambda: editing_setting_window.destroy(), font=("Times New Roman", 12))
                close_button.place(x=100, y=230)
                
                editing_setting_window.mainloop()
            except:
                messagebox.showerror("Ошибка", "Выберите строчку")
                editing_setting_window.destroy()

        setting_window = tk.Tk()
        setting_window.title(f"Настройки коммутатора {switch}")
        setting_window.geometry("820x400")
        setting_window.resizable(False, False)

        setting_table = ttk.Treeview(setting_window, show='headings', style="Main.Treeview")
        setting_table["height"] = 15 #число отображаемых строк]
        setting_table["columns"] = ("col0", "col1")
        setting_table.heading("col0", text="Настройка")
        setting_table.heading("col1", text="Значение")
        setting_table.column("col0", width=200) 
        setting_table.column("col1", width=600)
        for i in range(count_table): #тут число портов
            count = len(settings)
            if i < count:
                setting_table.insert("", tk.END, values=(settings[i]))
            else:
                setting_table.insert("", tk.END, values=())
                
        button = tk.Button(setting_window, text="Редактировать", command=lambda: setting_edit_button(), width=18, font="TimesNewRoman 10")
        button.place(x = 5, y = 350)
        
        vertical_scrolbar = ttk.Scrollbar(setting_window, orient="vertical", command=setting_table.yview)
        setting_table.configure(yscrollcommand=vertical_scrolbar.set)
        vertical_scrolbar.pack(side='right', fill='y')
        
        setting_table.pack(side='top', fill='both')
        setting_window.mainloop()


    #кнопка открывает таблицу MAC-адресов
    def mac_addr_table_button():
        cursor.execute(f"SELECT * FROM {switch}_mac_table")
        mac = cursor.fetchall()
        #кнопка для редактирования строки с маками
        def mac_addr_edit_button():
            cursor.execute(f"SELECT * FROM {switch}_mac_table")
            mac = cursor.fetchall()
            try:
                editing_mac_window = tk.Tk()
                editing_mac_window.title("Окно ввода MAC-адресов")
                editing_mac_window.geometry("600x300")
                editing_mac_window.resizable(False, False)
                
                #кнопка сохранить
                def save_button():  
                    note_text = note_mac.get('1.0', 'end')
                    cursor = connection.cursor() #ставим курсор
                    command = f"UPDATE {switch}_mac_table SET value = '{note_text}' WHERE number_port = {values[0]}" #команда
                    cursor.execute(command) #исполняем команду
                    connection.commit()
                    
                    selected_item_id = tree_mac_table.selection()[0]
                    tree_mac_table.item(selected_item_id, values=(values[0], note_text)) #данные для обновления
                    
                selected_port = tree_mac_table.selection()

                if selected_port:
                    values = tree_mac_table.item(selected_port)["values"]
                    

                label = tk.Label(editing_mac_window, text = f"Порт №{values[0]}", font=("Times New Roman", 12)) #номер порта
                label.pack()
                note_mac = tk.Text(editing_mac_window, font=("Times New Roman", 12), height = 10, width = 80)
                note_mac.insert(tk.END, mac[values[0]-1][1]) #-1 нужен потому что он брал значение на одну строку больше почему-то
                note_mac.pack()
      
                save_button = tk.Button(editing_mac_window, text = "Сохранить", command= save_button, font=("Times New Roman", 12))
                save_button.place(x=10, y=230)
                close_button = tk.Button(editing_mac_window, text = "Выход", command=lambda: editing_mac_window.destroy(), font=("Times New Roman", 12))
                close_button.place(x=100, y=230)
                
                editing_mac_window.mainloop()
            except:
                messagebox.showerror("Ошибка", "Выберите строчку")
                editing_mac_window.destroy()
        
        mac_addr_table = tk.Tk()
        mac_addr_table.title("Таблица статичных MAC-адресов")
        mac_addr_table.geometry("820x400")
        mac_addr_table.resizable(False, False)

        tree_mac_table = ttk.Treeview(mac_addr_table, show='headings', style="Main.Treeview")
        tree_mac_table["height"] = 15 #число отображаемых строк]
        tree_mac_table["columns"] = ("col0", "col1")
        tree_mac_table.heading("col0", text="№")
        tree_mac_table.heading("col1", text="Адреса")
        tree_mac_table.column("col0", width=50) 
        tree_mac_table.column("col1", width=750)
        for i in range(ports): #тут число портов
            count = len(mac)
            if i < count:
                tree_mac_table.insert("", tk.END, values=(mac[i]))
            else:
                tree_mac_table.insert("", tk.END, values=())
                
        button = tk.Button(mac_addr_table, text="Редактировать", command=lambda: mac_addr_edit_button(), width=18, font="TimesNewRoman 10")
        button.place(x = 5, y = 350)
        
        vertical_scrolbar = ttk.Scrollbar(mac_addr_table, orient="vertical", command=tree_mac_table.yview)
        tree_mac_table.configure(yscrollcommand=vertical_scrolbar.set)
        vertical_scrolbar.pack(side='right', fill='y')
        
        tree_mac_table.pack(side='top', fill='both')
        mac_addr_table.mainloop()

    def browser_button():
        ip = characteristics_data[0][1]
        webbrowser.open(f"http://{ip}", new=0, autoraise=True)

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

    addresses = ["Отключен", "Береговая, 18"] #сюда выгружаются данные из таблицы с адресами
    options = ttk.Combobox(mainframe, values=addresses, width=18, state='readonly')
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

    entry1 = tk.Entry(mainframe,width=18)
    entry1.place(x=120, y=30)
    entry2 = tk.Entry(mainframe,width=18)
    entry2.place(x=120, y=55)
    entry3 = tk.Entry(mainframe,width=18)
    entry3.place(x=120, y=80)
    button = tk.Button(mainframe, text=characteristics_data[0][4], command=lambda: None, width=18) #прописать функцию выбора локации
    button.place(x=120, y=105)
    entry5 = tk.Entry(mainframe,width=18)
    entry5.place(x=120, y=130)
    entry6 = tk.Entry(mainframe,width=18)
    entry6.place(x=120, y=155)
    entry7 = tk.Entry(mainframe,width=18)
    entry7.place(x=120, y=180)


    entry1.insert(0, characteristics_data[0][1])
    entry2.insert(0, characteristics_data[0][2])
    entry3.insert(0, characteristics_data[0][3])
    entry5.insert(0, characteristics_data[0][5])
    entry6.insert(0, characteristics_data[0][6])
    entry7.insert(0, characteristics_data[0][7])

    button1 = tk.Button(mainframe, text="Открыть в браузере", command=lambda: browser_button(), width=18, font="TimesNewRoman 10")
    button1.place(x=5, y=205)
    button2 = tk.Button(mainframe, text="Редактировать", command=lambda: edit_button(), width=18, font="TimesNewRoman 10")
    button2.place(x=180, y=205)
    button3 = tk.Button(mainframe, text="Таблица MAC-адресов", command=lambda: mac_addr_table_button(), width=18, font="TimesNewRoman 10")
    button3.place(x=5, y=250)
    button4 = tk.Button(mainframe, text="Настройки коммутатора", command=lambda: setting_switch_button(), width=18, font="TimesNewRoman 10")
    button4.place(x=180, y=250)
    button5 = tk.Button(mainframe, text="Сохр", command=lambda: save_settings_button(),width=4, height=2, font="TimesNewRoman 10")
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
