# База данных
import pyodbc 
connect = pyodbc.connect('''DRIVER=SQL Server;DATABASE=Treatment;Trusted_Connection=Yes;SERVER=DESKTOP-SDGD7CD\SQLEXPRESS;''')
cursor = connect.cursor()

from cab import cab
from pac import pac
from doc import doc
from tkinter import ttk
import tkinter as tk 

import sys
sys.path.insert(0, '../')
from main import main


main_window = tk.Tk()

tk.Button(text="Доктора", command=main).pack()
tk.Button(text="Отчет кабинеты", command=lambda : cab(cursor)).pack()
tk.Button(text="Отчет Пациенты", command=lambda : pac(cursor)).pack()

cursor.execute("""
	select txtDoctorName
	from tblDoctor
	""")
combo = ttk.Combobox(main_window, 
                            values=[i[0] for i in cursor])
combo.pack()
tk.Button(text="Отчет Доктор", command=lambda : doc(cursor,combo.get())).pack()

main_window.mainloop()