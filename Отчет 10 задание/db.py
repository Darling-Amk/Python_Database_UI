import pyodbc 

connect = pyodbc.connect(
            f'''
            DRIVER=SQL Server;
            DATABASE=Treatment;
            Trusted_Connection=Yes;
            SERVER=DESKTOP-SDGD7CD\SQLEXPRESS;
            ''')
cursor = connect.cursor()
cursor.execute(
           """
		Select txtTreatmentSetRoom, tblTreatmentVisit.datTreatmentVisitDate, tblPatient.txtPatientSecondName, tblPatient.txtPatientName, tblPatient.txtPatientSurname,tblTreatmentType.txtTreatmentTypeName
		From tblTreatmentSet ,tblTreatmentVisit,tblPatient,tblTreatmentType
		where tblTreatmentSet.intTreatmentSetId = tblTreatmentVisit.intTreatmentSetId and 
			tblTreatmentSet.intPatientId = tblPatient.intPatientId and 
			tblTreatmentSet.intTreatmentTypeId= tblTreatmentType.intTreatmentTypeId
		order by txtTreatmentSetRoom
	"""
    )

data = [ list([j for j in i]) for i in cursor]
data_ = {}

for e in data:
	if not(e[0] in data_):
		data_[e[0]] = list()

	data_[e[0]].append(e[1:])
