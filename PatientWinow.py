import tkinter as tk
import tkinter.font as font
from addwindow import AddWindow as aw
from ProcedureWindow import ProcedureWindow as pw


class PatientWindow():
    def __init__(self,db,line_count=11):
        self.line_count = line_count
        self.db=db

        self.PAGE_COUNTER = 1
        self.MAX_COUNTER = 1 +  self.db.get_count_line(name="tblPatient")//self.line_count
        self.PAGE_COUNTER_text = ""


    def __page_counter_update(self):
        self.PAGE_COUNTER_text.set(f"{self.PAGE_COUNTER}/{self.MAX_COUNTER}")
        self.MAX_COUNTER = 1 + self.db.get_count_line(name="tblPatient") // self.line_count


    def Show(self):
        self.root = tk.Toplevel()
        self.root.focus_set()
        self.root.grab_set()
        #self.root = tk.Tk()
        self.root.resizable(width=False, height=False)
        self.root.geometry("1050x680")
        self.root.title('Пациенты')
        self.PAGE_COUNTER_text = tk.StringVar()
        self.__draw_all()

    def __draw_all(self):
        tk.Canvas(self.root, height=130, width=1050, bg="#2cd997").pack()
        self.root['bg'] = '#f8f8f8'
        self.__draw_buttons()
        self.__draw_table()

    def next_page(self):
        self.PAGE_COUNTER = min(self.MAX_COUNTER, self.PAGE_COUNTER + 1)
        self.__page_counter_update()
        self.__update__table()

    def previous_page(self):
        self.PAGE_COUNTER = max(1, self.PAGE_COUNTER - 1)
        self.__page_counter_update()
        self.__update__table()

    def __draw_table(self):
        self.table = [[tk.Text(self.root, font=font.Font(size=16)) for i in range(self.line_count+1)] for j in range(3)]


        self.set_text(self.table[0][0], "ФИО пациента")
        self.set_text(self.table[1][0], "Дата Рождения")
        self.set_text(self.table[2][0], "Адрес")
        x = 0
        for i, collum in enumerate(self.table):
            y = 132
            for j, item in enumerate(collum):
                item.config(state='disabled')
                item.place(x=x, y=y, width=350, height=37)
                item.bind(f"<Double-Button-1>", lambda e,arg=j:self.open_func(e,arg))
                y += 37
            x += 350


        self.__update__table()

    def open_func(self,e,k):
        if k==0:
            return

        if len(self.last_db)<k:
            return
        # print(self.last_db[k-1])
        self.pw = pw(self.db,self.last_db[k-1])
        self.pw.show()

    def add_window(self):
        AddWindow = aw(self.db,(self.__update__table,self.__page_counter_update))
        AddWindow.Show()
        self.__page_counter_update()
        self.__update__table()

    def set_text(self,item,text):
        item.config(state=tk.NORMAL)
        item.tag_configure("center", justify='center')
        item.delete(1.0, tk.END)
        item.insert(1.0, text)
        item.tag_add("center", "1.0", "end")
        item.config(state='disabled')

    def __draw_buttons(self):
        tk.Button(self.root,
                  bg='#d99bff',
                  text="Add",
                  font=font.Font(size=28),
                  fg="#333333",
                  command=self.add_window
        ).place(x=750,y=25,width=250,height=80)

        tk.Label(self.root,
                 text='Пациенты',
                 bg="#2cd997",
                 font=font.Font(size=39, weight="bold"),
                 fg="#fff"
        ).place(x=25, y=32)

        tk.Label(self.root,
                textvariable=self.PAGE_COUNTER_text,
                bg="#f8f8f8"
        ).place(x=785 - 350,y=600,width=160,height=60)

        tk.Button(self.root,
                  bg='#85b6ff',
                  text="previous page",
                  font=font.Font(size=16),
                  fg="#333333",
                  command=self.previous_page
        ).place(x=85,y=600,width=160,height=60)

        tk.Button(self.root,
                  bg='#85b6ff',
                  text="next page",
                  font=font.Font(size=16),
                  fg="#333333",
                  command=self.next_page
        ).place(x=785, y=600, width=160, height=60)

        self.__page_counter_update()

    def __update__table(self):
        self.last_db = self.db.get_srez(name="intPatientid", last=self.line_count * self.PAGE_COUNTER, count=self.line_count-1,from_="tblPatient")
        parsed_db = [[""] * self.line_count for i in range(3)]
        for i, row in enumerate(self.last_db):
            parsed_db[0][i] = f"{row[2]} {row[3]} {row[4]}"
            parsed_db[1][i] = f"{row[5]}"
            parsed_db[2][i] = f"{row[6]}"

        for i, collum in enumerate(self.table):
            for j, item in enumerate(collum[1:]):
                self.set_text(item, parsed_db[i][j])


