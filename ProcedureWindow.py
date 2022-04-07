import tkinter as tk
import tkinter.font as font
from AddPatientWindow import AddPatientWindow as Apw

class ProcedureWindow:
    def __init__(self,db,user_info):
        self.user_info =user_info
        self.db = db
        self.user = user_info[0]
        self.line_count = 8

    def show(self):
        self.root = tk.Toplevel()
        self.root.focus_set()
        self.root.grab_set()
        self.root.resizable(width=False, height=False)
        self.root.geometry("1640x610")
        self.root.title(f'Процедуры: {self.user_info[2]} {self.user_info[3]} {self.user_info[4]}')

        self.PAGE_COUNTER = 1
        self.MAX_COUNTER = 1 + self.db.get_count_line_user(name="tblTreatmentSet",id_user=self.user,name_collum="intPatientID") // self.line_count
        self.PAGE_COUNTER_text = tk.StringVar()

        self.__draw_all()
    def __draw_all(self):
        tk.Canvas(self.root, height=180, width=1640, bg="#2cd997").pack()
        self.root['bg'] = '#f8f8f8'
        self.__draw_buttons()
        self.__draw_table()
    def __draw_buttons(self):
        tk.Button(self.root,
                  bg='#d99bff',
                  text="Add",
                  font=font.Font(size=28),
                  fg="#333333",
                  command=self.add_window
        ).place(x=1300,y=57,width=220,height=70)

        tk.Label(self.root,
                 text='Процедуры',
                 bg="#2cd997",
                 font=font.Font(size=64, weight="bold"),
                 fg="#fff"
        ).place(x=45, y=42)

        tk.Label(self.root,
                textvariable = self.PAGE_COUNTER_text,
                bg="#f8f8f8"
                 # bg="#000000"
        ).place(x=780,y=540,width=160,height=60)

        tk.Button(self.root,
                  bg='#85b6ff',
                  text="previous page",
                  font=font.Font(size=16),
                  fg="#333333",
                  command=self.previous_page
        ).place(x=20,y=540,width=160,height=60)

        tk.Button(self.root,
                  bg='#85b6ff',
                  text="next page",
                  font=font.Font(size=16),
                  fg="#333333",
                  command=self.next_page
        ).place(x=1460, y=540, width=160, height=60)

        self.__page_counter_update()
    def __draw_table(self):
        self.table = [[tk.Text(self.root, font=font.Font(size=12)) for i in range(self.line_count+1)] for j in range(6)]

        self.set_text(self.table[0][0], "Вид процедуры")
        self.set_text(self.table[1][0], "Дата начала курса")
        self.set_text(self.table[2][0], "Дата окончания курса")
        self.set_text(self.table[3][0], "Кол-во процедур(назначенных)")
        self.set_text(self.table[4][0], "Кол-во процедур(проведённых)")
        self.set_text(self.table[5][0], "Фио Доктора")
        x = 0
        for i, collum in enumerate(self.table):
            y = 180
            for j, item in enumerate(collum):
                item.config(state='disabled')
                item.place(x=x, y=y, width=273, height=37)
                y += 37
            x += 273
        self.__update__table()
    def set_text(self,item,text):
        item.config(state=tk.NORMAL)
        item.tag_configure("center", justify='center')
        item.delete(1.0, tk.END)
        item.insert(1.0, text)
        item.tag_add("center", "1.0", "end")
        item.config(state='disabled')
    def __page_counter_update(self):
        self.PAGE_COUNTER_text.set(f"{self.PAGE_COUNTER}/{self.MAX_COUNTER}")
        self.MAX_COUNTER = 1 + self.db.get_count_line_user(name="tblTreatmentSet", id_user=self.user,
                                                           name_collum="intPatientId") // self.line_count
    def next_page(self):
        self.PAGE_COUNTER = min(self.MAX_COUNTER, self.PAGE_COUNTER + 1)
        self.__page_counter_update()
        self.__update__table()
    def previous_page(self):
        self.PAGE_COUNTER = max(1, self.PAGE_COUNTER - 1)
        self.__page_counter_update()
        self.__update__table()
    def __update__table(self):
        db = self.db.execute(
            f'''
            SELECT txtTreatmentTypeName,datDateBegin,datDateEnd,intTreatmentSetCount,intTreatmentSetCountFact,txtDoctorName 
            FROM  tblTreatmentSet, tblDoctor,tblTreatmentType
            WHERE  (intPatientId = {self.user}) and
            (tblTreatmentSet.intDoctorId = tblDoctor.intDoctorId)     and
            (tblTreatmentSet.intTreatmentTypeId = tblTreatmentType.intTreatmentTypeId)
            '''
        )[self.line_count * (self.PAGE_COUNTER-1):self.line_count * (self.PAGE_COUNTER)]
        parsed_db = [[""] * self.line_count  for i in range(6)]
        # print(db)
        for i, row in enumerate(db):
            for j in range(6):
                parsed_db[j][i] = row[j]

        for i, collum in enumerate(self.table):
            for j, item in enumerate(collum[1:]):
                self.set_text(item, parsed_db[i][j])
    def add_window(self):
        AddPatientWindow = Apw(self.user,self.db, (self.__update__table, self.__page_counter_update))
        AddPatientWindow.Show()
        self.__page_counter_update()
        self.__update__table()