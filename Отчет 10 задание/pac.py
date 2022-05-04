from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, Paragraph,SimpleDocTemplate
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont #Import font

document = []
def pac(cursor):

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



	def get_all_for_id(id):
		cursor.execute(f"""
			SELECT 
			
			[txtTreatmentTypeName],[datDateBegin],[datDateEnd],[intTreatmentSetCount],[intTreatmentSetCountFact],[intTreatmentSetCount]-[intTreatmentSetCountFact] as 'intTreatmentDiffCount',[txtTreatmentSetRoom]	
	  		FROM [tblTreatmentSet] ,tblPatient,tblTreatmentType
	  		where tblPatient.intPatientId = tblTreatmentSet.intPatientId and tblTreatmentType.intTreatmentTypeId = tblTreatmentSet.intTreatmentTypeId and tblTreatmentSet.intPatientId = {id}

			"""
			)
		return  [i for i in cursor]


	def get_all_pac():
		cursor.execute(f"""
			select *
			from tblPatient
			""")
		return [i for i in cursor]

	# count = 0 
	for pac in get_all_pac():
		id,f,i,o,date,address = pac
		printf(f"ФИО: {f} {i} {o}")
		printf(f"Дата рождения: {date}")
		printf(f"Адрес: {address}")
		t = get_all_for_id(id)
		if(t):add_table([("Процедура","Начало","Окончание","Назначено","Проведено","Осталось","Кабинет")]+t)


		printf("-"*68)


	SimpleDocTemplate("Пациенты.pdf",title='Пациенты').build(document)
	print("Отчет напечатан")
