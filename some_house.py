import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import mysql.connector
from tkinter import messagebox
from PIL import ImageTk, Image

#beregovaya_16 и beregovaya_16_characteristics
#сделать форму универсальной, для чего в перменную записываются названия домов и передаются в функцию;
#названия фотографий будут переданы через соответствия в словаре через ключ-значение

residential_houses = ["beregovaya_16"]
residential_houses_characteristics = ["beregovaya_16_characteristics"]

house = residential_houses[0] #будет заменено
house_characteristics = residential_houses_characteristics[0] #будет заменено

connection = mysql.connector.connect(
host="192.168.58.240",
user="admin",
passwd="MiloRd12",
database="nnc_db")
cursor = connection.cursor() #ставим курсор

def rundom_house():
    cursor.execute(f"SELECT * FROM {house}")
    main_data = cursor.fetchall()
    cursor.execute(f"SELECT * FROM {house_characteristics}")
    characteristics_data = cursor.fetchall()
    #print([i[0] for i in cursor.description])
    #print(characteristics_data)
            
    heading = ["ID", "Оборудование", "Подъезд", "Этаж", "Сетевое имя", "Марка", "Исходящее соединение", "Входящее соединение"]

    def save_note():
        note_text = note.get('1.0', 'end')
        cursor = connection.cursor() #ставим курсор
        command = f"UPDATE {house_characteristics} SET Note = '{note_text}'" #команда
        cursor.execute(command) #исполняем команду
        connection.commit()

    def edit_button():
        try:
            editing_window = tk.Tk()
            editing_window.title("Окно редактирования")
            editing_window.geometry("350x250")

            def save_button():  
                #оптимизировать 1
                value1 = entry1.get()
                value2 = entry2.get()
                value3 = entry3.get()
                value4 = entry4.get()
                value5 = entry5.get()
                value6 = entry6.get()
                value7 = entry7.get()

                cursor = connection.cursor() #ставим курсор
                
                command = f"UPDATE {house} SET Equipment = '{value1}', Entrance = '{value2}', Floor = '{value3}', Network_name = '{value4}', Brand = '{value5}', Outgoing_connection = '{value6}', Incoming_connection = '{value7}' WHERE ID = {values[0]}" #команда
                cursor.execute(command) #исполняем команду
                connection.commit()
                
                selected_item_id = tree.selection()[0]
                tree.item(selected_item_id, values=(values[0], value1, value2, value3, value4, value5, value6, value7)) #данные для обновления

            selected_item = tree.selection()
            
            if selected_item:
                values = tree.item(selected_item)["values"]

            for row, head in zip(range(0, len(heading)), heading):
                label = tk.Label(editing_window, text=head, font=("Times New Roman", 12))
                label.grid(row=row, column=0)
            
            id = tk.Label(editing_window, text = values[0], font=("Times New Roman", 12), relief="groove", width=17, height=1)
            id.grid(row=0, column=1)
            
            #оптимизировать 2
            entry1 = tk.Entry(editing_window, font=("Times New Roman", 12))
            entry1.grid(row=1, column=1)
            entry1.insert(0, values[1])
            entry2 = tk.Entry(editing_window, font=("Times New Roman", 12))
            entry2.grid(row=2, column=1)
            entry2.insert(0, values[2])
            entry3 = tk.Entry(editing_window, font=("Times New Roman", 12))
            entry3.grid(row=3, column=1)
            entry3.insert(0, values[3])
            entry4 = tk.Entry(editing_window, font=("Times New Roman", 12))
            entry4.grid(row=4, column=1)
            entry4.insert(0, values[4])
            entry5 = tk.Entry(editing_window, font=("Times New Roman", 12))
            entry5.grid(row=5, column=1)
            entry5.insert(0, values[5])
            entry6 = tk.Entry(editing_window, font=("Times New Roman", 12))
            entry6.grid(row=6, column=1)
            entry6.insert(0, values[6])
            entry7 = tk.Entry(editing_window, font=("Times New Roman", 12))
            entry7.grid(row=7, column=1)
            entry7.insert(0, values[7])

            save_button = tk.Button(editing_window, text = "Сохранить", command= save_button, font=("Times New Roman", 12))
            save_button.place(x=10, y=200)
            close_button = tk.Button(editing_window, text = "Выход", command=lambda: editing_window.destroy(), font=("Times New Roman", 12))
            close_button.place(x=100, y=200)
            
            editing_window.mainloop()
        except:
            messagebox.showerror("Ошибка", "Выберите строчку")
            editing_window.destroy()

    def open_img():
        path = r'Images/Bereg_16.png'
        root1 = tk.Toplevel()
        root1.title(f'План - схема распределительной Ethernet сети "{characteristics_data[0][0]}" ')
        root1.geometry("1500x500")
        root1.resizable(True, True)
        
        img = ImageTk.PhotoImage(Image.open(path))
        label1 = tk.Label(root1, image=img)
        label1.image = img
        label1.pack()
        root1.mainloop()

    def open_img_1():
        path = r'Images/Bereg_16_1.png'
        root1 = tk.Toplevel()
        root1.title(f'Схема подключения дома "{characteristics_data[0][0]}" ')
        root1.geometry("1500x500")
        root1.resizable(True, True)
        
        img = ImageTk.PhotoImage(Image.open(path))
        label1 = tk.Label(root1, image=img)
        label1.image = img
        label1.pack()
        root1.mainloop()

    root = tk.Tk()
    root.title(f'Панель дома "{characteristics_data[0][0]}"')
    root.geometry("1150x600")
    root.resizable(False, False)

    #оптимизировать 3
    label1 = tk.Label(root, text="Адрес", font=("Times New Roman", 12), width=15, height=1, relief="ridge", borderwidth = 3, fg="#eee", bg="gray14").grid(row=0, column=0)
    label2 = tk.Label(root, text="Абоненты", font=("Times New Roman", 12), width=15, height=1, relief="ridge", borderwidth = 3, fg="#eee", bg="gray14").grid(row=1, column=0)
    label3 = tk.Label(root, text="Оборудование", font=("Times New Roman", 15)).grid(row=2, column=0, columnspan=2)
    label4 = tk.Label(root, text="Коммутаторы", font=("Times New Roman", 10), width=20, height=1, relief="ridge", borderwidth = 3, fg="#eee", bg="gray14").grid(row=3, column=0)
    label5 = tk.Label(root, text="ADSL-модемы", font=("Times New Roman", 10), width=20, height=1, relief="ridge", borderwidth = 3, fg="#eee", bg="gray14").grid(row=4, column=0)
    label6 = tk.Label(root, text="VDSL-модемы", font=("Times New Roman", 10), width=20, height=1, relief="ridge", borderwidth = 3, fg="#eee", bg="gray14").grid(row=5, column=0)
    label7 = tk.Label(root, text="Медиаконвертеры", font=("Times New Roman", 10), width=20, height=1, relief="ridge", borderwidth = 3, fg="#eee", bg="gray14").grid(row=6, column=0)
    label8 = tk.Label(root, text="SFP-модули", font=("Times New Roman", 10), width=20, height=1, relief="ridge", borderwidth = 3, fg="#eee", bg="gray14").grid(row=7, column=0)

    #оптимизировать 4
    label1_1 = tk.Label(root, text=characteristics_data[0][0], font=("Times New Roman", 12))
    label1_1.grid(row=0, column=1)
    label2_1 = tk.Label(root, text=characteristics_data[0][1], font=("Times New Roman", 12))
    label2_1.grid(row=1, column=1)
    label3_1 = tk.Label(root, text="Оборудование", font=("Times New Roman", 15))
    label3_1.grid(row=2, column=0, columnspan=2)
    label4_1 = tk.Label(root, text=characteristics_data[0][2], font=("Times New Roman", 12))
    label4_1.grid(row=3, column=1)
    label5_1 = tk.Label(root, text=characteristics_data[0][3], font=("Times New Roman", 12))
    label5_1.grid(row=4, column=1)
    label6_1 = tk.Label(root, text=characteristics_data[0][4], font=("Times New Roman", 12))
    label6_1.grid(row=5, column=1)
    label7_1 = tk.Label(root, text=characteristics_data[0][5], font=("Times New Roman", 12))
    label7_1.grid(row=6, column=1)
    label8_1 = tk.Label(root, text=characteristics_data[0][6], font=("Times New Roman", 12))
    label8_1.grid(row=7, column=1)

    
    """row_num_1 = range(0, 2)
    row_num_2 = range(3, 8)

    for value, row in zip(characteristics_data[0][:2], row_num_1):
        label = tk.Label(root, text=value, font=("Times New Roman", 12))
        label.grid(row=row, column=1)

    for value, row in zip(characteristics_data[0][2:], row_num_2):
        label = tk.Label(root, text=value, font=("Times New Roman", 12))
        label.grid(row=row, column=1)"""

    note = tk.Text(root, font=("Times New Roman", 12))
    note.insert(tk.END, characteristics_data[0][7])
    note.place(x=400, y=10)

    style = ttk.Style()
    
    style.theme_use("classic")
    style.configure("Main.Treeview", background="white", foreground="black", font=("Times New Roman", 12), rowheight=30)
    style.configure('Heading', background="black", foreground="white", font=("Times New Roman", 12))
    
    tree = ttk.Treeview(root, show='headings', style="Main.Treeview")
    tree["columns"] = ("col0", "col1", "col2", "col3", "col4", "col5", "col6", "col7")

    heading_range = range(9)
    
    #заголовки
    for row, head in zip(heading_range, heading):
        tree.heading(f"col{row}", text=head)
        if row == 0:
            tree.column("col0", width=10)
        elif row == 1:
            tree.column("col1", width=150)
        elif row == 2:
            tree.column("col2", width=70)
        elif row == 3:
            tree.column("col3", width=70)
        elif row == 4:
            tree.column("col4", width=150)
        elif row == 5:
            tree.column("col5", width=350) 
        elif row == 6:
            tree.column("col6", width=150)
        elif row == 7:
            tree.column("col7", width=150)
    
    for i in range(20): #тут число строчек
        count = len(main_data)
        if i < count:
            tree.insert("", tk.END, values=(main_data[i]))
        else:
            tree.insert("", tk.END, values=())

    cursor.close() #закрываем курсор
    #connection.close() #закрываем соединение (тот момент стоит обдумать в будущем))
    
    tree.place(x=1, y=210)

    edit_button = tk.Button(root, text="Редактировать", command=edit_button)
    edit_button.place(x=1, y=555)
    button1 = tk.Button(root, text="Схема сети", command=lambda: open_img()) #кнопка схемы сети
    button1.place(x=150, y=555)    
    button2 = tk.Button(root, text="Схема подключения", command=lambda: open_img_1()) #кнопка схемы подключения
    button2.place(x=250, y=555)    
    button3 = tk.Button(root, text = "S", width=3, height=2, command=lambda: save_note()) #кнопка сохранения заметки
    button3.place(x=1050, y=150)  

    #оптимизировать 5
    #кнопки болье-меньше
    def button_click(btn_id):
        if btn_id == 1:
            cursor = connection.cursor() #ставим курсор
            cursor.execute(f"SELECT Subscribers FROM {house_characteristics}")
            data = cursor.fetchall()
            value = int(data[0][0]) + 1
            command = f"UPDATE {house_characteristics} SET Subscribers = '{value}'" #команда
            cursor.execute(command) #исполняем команду
            connection.commit()
            label2_1.config(text=int(value))
            label2_1.grid(row=1, column=1)
        elif btn_id == 2:
            cursor = connection.cursor() #ставим курсор
            cursor.execute(f"SELECT Subscribers FROM {house_characteristics}")
            data = cursor.fetchall()
            value = int(data[0][0]) - 1
            command = f"UPDATE {house_characteristics} SET Subscribers = '{value}'" #команда
            cursor.execute(command) #исполняем команду
            connection.commit()
            label2_1.config(text=int(value))
            label2_1.grid(row=1, column=1)
        elif btn_id == 3:
            cursor = connection.cursor() #ставим курсор
            cursor.execute(f"SELECT Switches FROM {house_characteristics}")
            data = cursor.fetchall()
            value = int(data[0][0]) + 1
            command = f"UPDATE beregovaya_16_characteristics SET Switches = '{value}'" #команда
            cursor.execute(command) #исполняем команду
            connection.commit()
            label4_1.config(text=int(value))
            label4_1.grid(row=3, column=1)
        elif btn_id == 4:
            cursor = connection.cursor() #ставим курсор
            cursor.execute(f"SELECT Switches FROM {house_characteristics}")
            data = cursor.fetchall()
            value = int(data[0][0]) - 1
            command = f"UPDATE {house_characteristics} SET Switches = '{value}'" #команда
            cursor.execute(command) #исполняем команду
            connection.commit()
            label4_1.config(text=int(value))
            label4_1.grid(row=3, column=1)
        elif btn_id == 5:
            cursor = connection.cursor() #ставим курсор
            cursor.execute(f"SELECT ADSL_modems FROM {house_characteristics}")
            data = cursor.fetchall()
            value = int(data[0][0]) + 1
            command = f"UPDATE {house_characteristics} SET ADSL_modems = '{value}'" #команда
            cursor.execute(command) #исполняем команду
            connection.commit()
            label5_1.config(text=int(value))
            label5_1.grid(row=4, column=1)
        elif btn_id == 6:
            cursor = connection.cursor() #ставим курсор
            cursor.execute(f"SELECT ADSL_modems FROM {house_characteristics}")
            data = cursor.fetchall()
            value = int(data[0][0]) - 1
            command = f"UPDATE {house_characteristics} SET ADSL_modems = '{value}'" #команда
            cursor.execute(command) #исполняем команду
            connection.commit()
            label5_1.config(text=int(value))
            label5_1.grid(row=4, column=1)
        elif btn_id == 7:
            cursor = connection.cursor() #ставим курсор
            cursor.execute(f"SELECT VDSL_modems FROM {house_characteristics}")
            data = cursor.fetchall()
            value = int(data[0][0]) + 1
            command = f"UPDATE {house_characteristics} SET VDSL_modems = '{value}'" #команда
            cursor.execute(command) #исполняем команду
            connection.commit()
            label6_1.config(text=int(value))
            label6_1.grid(row=5, column=1)
        elif btn_id == 8:
            cursor = connection.cursor() #ставим курсор
            cursor.execute(f"SELECT VDSL_modems FROM {house_characteristics}")
            data = cursor.fetchall()
            value = int(data[0][0]) - 1
            command = f"UPDATE {house_characteristics} SET VDSL_modems = '{value}'" #команда
            cursor.execute(command) #исполняем команду
            connection.commit()
            label6_1.config(text=int(value))
            label6_1.grid(row=5, column=1)
        elif btn_id == 9:
            cursor = connection.cursor() #ставим курсор
            cursor.execute(f"SELECT Mediaconverters FROM {house_characteristics}")
            data = cursor.fetchall()
            value = int(data[0][0]) + 1
            command = f"UPDATE {house_characteristics} SET Mediaconverters = '{value}'" #команда
            cursor.execute(command) #исполняем команду
            connection.commit()
            label7_1.config(text=int(value))
            label7_1.grid(row=6, column=1)
        elif btn_id == 10:
            cursor = connection.cursor() #ставим курсор
            cursor.execute(f"SELECT Mediaconverters FROM {house_characteristics}")
            data = cursor.fetchall()
            value = int(data[0][0]) - 1
            command = f"UPDATE {house_characteristics} SET Mediaconverters = '{value}'" #команда
            cursor.execute(command) #исполняем команду
            connection.commit()
            label7_1.config(text=int(value))
            label7_1.grid(row=6, column=1)
        elif btn_id == 11:
            cursor = connection.cursor() #ставим курсор
            cursor.execute(f"SELECT SFP_modules FROM {house_characteristics}")
            data = cursor.fetchall()
            value = int(data[0][0]) + 1
            command = f"UPDATE {house_characteristics} SET SFP_modules = '{value}'" #команда
            cursor.execute(command) #исполняем команду
            connection.commit()
            label8_1.config(text=int(value))
            label8_1.grid(row=7, column=1)
        elif btn_id == 12:
            cursor = connection.cursor() #ставим курсор
            cursor.execute(f"SELECT SFP_modules FROM {house_characteristics}")
            data = cursor.fetchall()
            value = int(data[0][0]) - 1
            command = f"UPDATE {house_characteristics} SET SFP_modules = '{value}'" #команда
            cursor.execute(command) #исполняем команду
            connection.commit()
            label8_1.config(text=int(value))
            label8_1.grid(row=7, column=1)

    #кнопки больше-меньше
    buttons = []
    button_positions = [(28, "+", button_click), (28, "-", button_click), (80, "+", button_click), (80, "-", button_click),
                        (105, "+", button_click), (105, "-", button_click), (130, "+", button_click), (130, "-", button_click),
                        (155, "+", button_click), (155, "-", button_click), (180, "+", button_click), (180, "-", button_click)]

    for index, (y, text, command) in enumerate(button_positions):
        button = tk.Button(root, text=text, command=lambda index=index: button_click(index+1))
        button.place(x=160 if index % 2 == 1 else 210, y=y)
        buttons.append(button)
     
    #полоса прокрутки
    vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.place(x=1130, y=200, height=400)

    root.mainloop()

rundom_house()
