from database_class import DataBase
from PatientWinow import PatientWindow as pw
from addwindow import AddWindow as aw

import tkinter as tk

def main():
    db = DataBase(name="Treatment")
    # main_window = tk.Tk()
    # main_window.resizable(width=False, height=False)
    # main_window.geometry("1050x680")
    # main_window.title("main window")
    PatientWindow = pw(db)
    PatientWindow.Show()
    # tk.Button(command=PatientWindow.Show,text="Пациент").pack()
    # tk.Button(command=PatientWindow.Show, text="Пациент").pack()
    PatientWindow.root.mainloop()

if __name__=='__main__':
    main()


