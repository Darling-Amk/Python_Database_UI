from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, Paragraph,SimpleDocTemplate
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont #Import font

document = []
def doc(cursor,name):

	#global settings
	pdfmetrics.registerFont(TTFont('Bitter-Regular','Bitter-Regular.ttf', 'UTF-8')) #Register font
	styles = getSampleStyleSheet()
	styles['BodyText'].fontName='Bitter-Regular'
	style = styles["BodyText"]

	# Запись в документ

	def printf(text):
		global document
		document.append(Paragraph(f"<bold><font size=14>{text}</font></bold>",style))
		document.append(Paragraph(f"",style))

	def add_table(data):
		global document
		data = [ list([Paragraph(str(j),styles["BodyText"]) for j in i]) for i in data]
		t = Table(data)
		t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))
		for each in range(len(data)):
		    if each % 2 == 0:bg_color = colors.whitesmoke
		    else:bg_color = colors.lightgrey
		    t.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))
		document.append(t)


	cursor.execute(f"""
		select intDoctorId,txtSpecialist,datDoctorWork
		from tblDoctor
		where txtDoctorName ='{name}';
		""")
	id,spec,date = [i for i in cursor][0]
	printf(f"{name}")
	printf(f"{spec}")
	printf(f"{date}")
	cursor.execute(f"""
		SELECT [txtPatientSurname],[txtPatientName],[txtPatientSecondName],

	  txtTreatmentTypeName,[datDateBegin],[datDateEnd]
	  
  	FROM tblDoctor,tblTreatmentSet,tblPatient,tblTreatmentType
  	where tblDoctor.intDoctorId = {id} and
  	tblTreatmentSet.intDoctorId = tblDoctor.intDoctorId and 
  	tblTreatmentSet.intPatientId = tblPatient.intPatientId and
  	tblTreatmentSet.intTreatmentTypeId = tblTreatmentType.intTreatmentTypeId
  	order by [txtPatientSurname],[txtPatientName],[txtPatientSecondName];
		""")
	add_table([("Фамилия","Имя","Отчество","Тип","Начало","Конец")]+[i for i in cursor])



	SimpleDocTemplate("Доктор.pdf",title='Доктор').build(document)
	print("Отчет напечатан")
