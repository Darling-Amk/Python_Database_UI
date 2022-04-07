import tkinter as tk
from tkinter import font
class AddWindow():
    def __init__(self,db,update):
        self.db = db
        self.update = update

    def Show(self):
        self.root = tk.Toplevel()
        self.root.focus_set()
        self.root.grab_set()
        self.root.resizable(width=False, height=False)
        self.root.geometry("730x320")
        self.root.title('Добавить пациента')

        self.__draw_all()

    def __draw_all(self):
        tk.Canvas(self.root, height=85, width=730, bg="#2cd997").pack()
        self.root['bg'] = '#f8f8f8'
        self.__draw_button()
        self.__draw_record()


    def __draw_button(self):
        tk.Button(self.root,
                  bg='#2cd997',
                  text="Add",
                  font=font.Font(size=18),
                  fg="#333333",
                  command=self.__add
        ).place(x=540,y=230,width=160,height=70)

    def __add(self):
        fio = self.fio.get("1.0",tk.END).split()
        date = str(self.date.get("1.0",tk.END)).replace("\n","")
        address = str(self.address.get("1.0", tk.END))
        if len(fio)==3 and len(date)!=0 and len(address)!=0:
            txtPatientSurname,txtPatientName , txtPatientSecondName = fio
            try:
                self.db.insert(
                    id='intPatientId',
                    name="Treatment.dbo.tblPatient",
                    txtPatientSurname=f"'{txtPatientSurname}'",
                    txtPatientName=f"'{txtPatientName}'",
                    txtPatientSecondName=f"'{txtPatientSecondName}'",
                    datBirthday=f"'{date}'",
                    txtAddress=f"'{address}'"
                )
                self.update[0]()
                self.update[1]()
                self.fio.delete('1.0', tk.END)
                self.date.delete('1.0', tk.END)
                self.address.delete('1.0', tk.END)

            except:
                print('Error to connect')

    def __draw_record(self):
        tk.Label(self.root, text='Новый пациенты',bg="#2cd997",font=font.Font(size=25, weight="bold"),fg="#fff"
                 ).place(x=20, y=22)
        tk.Label(self.root,bg='#f8f8f8',text='ФИО',font=font.Font(size=22),fg="#333333"
                 ).place(x=20, y=100)
        tk.Label(self.root,bg='#f8f8f8',text='Дата рождения',font=font.Font(size=22),fg="#333333"
                 ).place(x=20, y=170)
        tk.Label(self.root,bg='#f8f8f8',text='Адрес',font=font.Font(size=22),fg="#333333"
                 ).place(x=20, y=240)

        self.fio = tk.Text(self.root,bg='#c4c4c4',font=font.Font(size=14),fg="#fff")
        self.fio.place(x=245, y=100,width=260,height=50)

        self.date = tk.Text(self.root,bg='#c4c4c4',font=font.Font(size=14),fg="#fff")
        self.date.place(x=245, y=170, width=260, height=50)

        self.address = tk.Text(self.root,bg='#c4c4c4',font=font.Font(size=14),fg="#fff")
        self.address.place(x=245, y=240, width=260, height=50)