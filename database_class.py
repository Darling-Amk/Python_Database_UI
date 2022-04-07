import pyodbc

class DataBase():
    def __init__(self,name):
        # self.connect = pyodbc.connect(driver='{SQL Server Native Client 10.0}', server='192.168.112.103',
        #                               database='db22203', user='User016', password='User016#{61')
        self.connect = pyodbc.connect(
            f'''
            DRIVER=SQL Server;
            DATABASE={name};
            Trusted_Connection=Yes;
            SERVER=DESKTOP-SDGD7CD\SQLEXPRESS;
            ''')
        self.cursor = self.connect.cursor()

    def get_count_line(self,name):
        self.cursor.execute(
            f"""
            SELECT COUNT(*)  
            FROM {name}
            """
        )
        return self.cursor.fetchone()[0]

    def get_count_line_user(self,name,id_user,name_collum):

        self.cursor.execute(
            f"""
            SELECT COUNT(*)  
            FROM {name}
            WHERE {name_collum} = {id_user}
            """
        )
        return self.cursor.fetchone()[0]

    def get_srez(self,name,last,count,from_):
        self.cursor.execute(
            f"""
            WITH num_row
            AS
            (
            SELECT row_number() OVER (ORDER BY {name}) as nom , *
            FROM {from_}
            )
            SELECT * FROM num_row
            WHERE nom BETWEEN ({last} - {count}) AND {last}
            """
        )
        res = []
        for i in self.cursor:
            res.append(i)
        return res

    def execute(self,execute:str,type="SELECT")->list:
        self.cursor.execute(
            execute
        )

        res = []
        if type!="insert":
            for i in self.cursor:
                res.append(i)
        self.cursor.commit()
        return res

    def get_max_val_in_collum(self,name,collum):
        self.cursor.execute(
            f'''
            SELECT MAX({collum})
            FROM {name}
            '''
        )
        return self.cursor.fetchone()[0]

    def insert(self,**kwarg):
        columns=''
        values=''

        name = kwarg['name']
        for key,el in kwarg.items():
            if key=='name':
                continue
            if key=='id':
                columns += f'{el},'
                values += f'{self.get_max_val_in_collum(name=name,collum=el)+1},'
                continue
            columns+=f'{key},'
            values +=f'{el},'


        self.cursor.execute(
        f"""
            INSERT  INTO {name}
            ({columns[:-1]})
            VALUES
            ({values[:-1]})
        """
        )
        self.cursor.commit()