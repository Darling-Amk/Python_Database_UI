import tkinter as tk
from tkinter import font
from tkcalendar import Calendar
from tkinter import ttk
from datetime import datetime

class AddPatientWindow():
    def __init__(self,user,db,update):
        self.db = db
        self.user = user
        self.update = update

        self.getAllForUser()
    def getAllForUser(self):

        self.name,self.surname,self.secondname,self.birthday= self.db.execute(f'''
            SELECT txtPatientName,txtPatientSurname,txtPatientSecondName,datBirthday
            FROM tblPatient
            Where intPatientId = {self.user}
        ''')[0]
        doctors_list = self.db.execute(f'''
            SELECT intDoctorId,txtDoctorName
            FROM tblDoctor
        ''')
        self.doctors_dict = {e2:e1 for e1,e2 in doctors_list}
        self.doctors_values = [e2 for e1,e2 in doctors_list]

        procedures_list = self.db.execute(f'''
                   SELECT intTreatmentTypeId,txtTreatmentTypeName
                   FROM tblTreatmentType
               ''')
        # print(procedures_list)

        self.procedures_dict = {e2: e1 for e1, e2 in procedures_list}
        self.procedures_values = [e2 for e1, e2 in procedures_list]


        self.cabinets_values = [f"{i}" for i in range(1,10)]

    def Show(self):
        self.root = tk.Toplevel()
        self.root.focus_set()
        self.root.grab_set()
        self.root.resizable(width=False, height=False)
        self.root.geometry("1230x780")
        self.root.title('Добавить пациента')

        self.__draw_all()
    def __draw_all(self):
        tk.Canvas(self.root, height=130, width=1230, bg="#2cd997").pack()
        self.root['bg'] = '#f8f8f8'
        self.__draw_button()
        self.__draw_record()
    def __draw_button(self):
        tk.Button(self.root,
                  bg='#2cd997',
                  text="Add",
                  font=font.Font(size=16),
                  fg="#333333",
                  command=self.__add
        ).place(x=950,y=670,width=260,height=90)
    def __draw_record(self):
        self.info = tk.Text(self.root,bg='#c4c4c4',font=font.Font(size=26),fg="#1f1b1b")
        self.set_text(self.info,f"\n {self.surname}\n {self.name}\n {self.secondname}\n\n {self.birthday}",center=False)
        self.info.place(x=950, y=150, width=260, height=500)

        self.cal1,self.cal2 = self.__draw_calendar(240,400),self.__draw_calendar(540,400)

        tk.Label(self.root,
                 text='Назначение процедуры ',
                 bg="#2cd997",
                 font=font.Font(size=39, weight="bold"),
                 fg="#fff"
                 ).place(x=25, y=32)

        tk.Label(self.root, text='Вид процедуры', bg="#f8f8f8",font=font.Font(size=24),fg="#333333"
                 ).place(x=35, y=180)
        tk.Label(self.root, text='Доктор', bg="#f8f8f8",font=font.Font(size=24),fg="#333333"
                 ).place(x=35+120, y=260)

        self.procedure = ttk.Combobox(self.root,
                                    state="readonly",
                                    values=self.procedures_values,
                                    font=font.Font(size=24)
                                    )
        self.procedure.place(x=265, y=180, width=500, height=50)

        self.doctors = ttk.Combobox(self.root,
                                    state="readonly",
                                    values=self.doctors_values,
                                    font=font.Font(size=24)
                                                )
        self.doctors.place(x=265, y=260, width=500, height=50)

        tk.Label(self.root, text='Дата начала', bg="#f8f8f8",font=font.Font(size=22),fg="#333333"
                 ).place(x=275, y=350)
        tk.Label(self.root, text='Дата окончания', bg="#f8f8f8",font=font.Font(size=22),fg="#333333"
                 ).place(x=255+300, y=350)



        tk.Label(self.root, text='Количество процедур', bg="#f8f8f8",font=font.Font(size=22),fg="#333333"
                 ).place(x=35+120, y=670)
        self.procedure_count = ttk.Spinbox(self.root,from_=1,to=30,font=font.Font(size=22))
        self.procedure_count.place(x=460, y=670, width=100, height=40)

        tk.Label(self.root, text='Кабинет', bg="#f8f8f8",font=font.Font(size=22),fg="#333333"
                 ).place(x=600, y=670)

        self.cabinet = ttk.Combobox(self.root,
                                    state="readonly",
                                    values=self.cabinets_values,
                                    font=font.Font(size=22)
                                    )
        self.cabinet.place(x=730, y=670, width=50, height=40)
    def set_text(self,item,text,center=True):
        item.config(state=tk.NORMAL)
        item.tag_configure("center", justify='center')
        item.delete(1.0, tk.END)
        item.insert(1.0, text)
        if center:
            item.tag_add("center", "1.0", "end")
        item.config(state='disabled')
    def __add(self):
        intDoctorId = int(self.getDoctorId(self.doctors.get()))
        intPatientId = int(self.user)
        datDateBegin = self.date_to_datetime(self.cal1.get_date())
        datDateEnd = self.date_to_datetime(self.cal2.get_date())
        datDateBegin,datDateEnd = self.valid_date(datDateBegin,datDateEnd)
        txtTreatmentSetRoom = f'{str(self.cabinet.get())}'
        intTreatmentSetCount = self.procedure_count.get()
        if intTreatmentSetCount:
            intTreatmentSetCount = int(intTreatmentSetCount)
        intTreatmentSetCountFact = 0
        intTreatmentTypeId = int(self.getProcedureID(self.procedure.get()))

        # print("\n\n\n\n\n\n\n")
        # print(f'[+] DoctorID:{intDoctorId}')
        # print(f'[+] UserId:{intPatientId}')
        # print(f'[+] First date:{datDateBegin}')
        # print(f'[+] Second date:{datDateEnd}')
        # print(f'[+] Cabinet:{txtTreatmentSetRoom}')
        # print(f'[+] Count:{intTreatmentSetCount}')
        # print(f'[+] CountFact:{intTreatmentSetCountFact}')
        # print(f'[+] ProcedureId:{intTreatmentTypeId}')

        if all([intDoctorId,intPatientId,datDateBegin,datDateEnd,txtTreatmentSetRoom,intTreatmentSetCount,intTreatmentTypeId]):
            print(f"""
                    INSERT INTO tblTreatmentSet
                    (intDoctorId,intPatientId,datDateBegin,datDateEnd,txtTreatmentSetRoom,intTreatmentSetCount,intTreatmentSetCountFact,intTreatmentTypeId)
                    Values
                    ({intDoctorId},{intPatientId},{datDateBegin},{datDateEnd},{txtTreatmentSetRoom},{intTreatmentSetCount},{intTreatmentSetCountFact},{intTreatmentTypeId});
                """)
            self.db.execute(
                f"""
                    INSERT INTO tblTreatmentSet
                    (intDoctorId,intPatientId,datDateBegin,datDateEnd,txtTreatmentSetRoom,intTreatmentSetCount,intTreatmentSetCountFact,intTreatmentTypeId)
                    Values
                    ({intDoctorId},{intPatientId},'{datDateBegin}','{datDateEnd}','{txtTreatmentSetRoom}',{intTreatmentSetCount},{intTreatmentSetCountFact},{intTreatmentTypeId});
                """,
            type="insert")
            self.update[0]()
            self.update[1]()
    def __draw_calendar(self,x,y):
        now = datetime.now()
        year,month,day = map(int,now.strftime("%Y-%m-%d").split("-"))
        cal = Calendar(self.root,selectmode='day',
                            year=year,month=month,
                            day=day)
        cal.place(x=x,y=y)
        return cal
    def getDoctorId(self,Doctorname):
        if Doctorname in self.doctors_dict:
            return self.doctors_dict[Doctorname]
        return  False
    def getProcedureID(self,Procudurename):
        if Procudurename in self.procedures_dict:
            return self.procedures_dict[Procudurename]
        return False
    def date_to_datetime(self,date):
        mouth,day,year = date.split('/')
        return  datetime(int("20"+year), int(mouth), int(day))
    def valid_date(self,date1,date2):
        now = datetime.now()

        if date1<now or date2<now or date1>date2:
            # print(date1,date2,now)
            return  False,False
        return date1.strftime("%Y-%m-%d"),date2.strftime("%Y-%m-%d")