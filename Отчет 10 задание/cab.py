from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, Paragraph,SimpleDocTemplate
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont #Import font

document = []
def cab(cursor):
	def get_for_cab(number):
		cursor.execute(
		           f"""
				Select tblTreatmentVisit.datTreatmentVisitDate, tblPatient.txtPatientSecondName, tblPatient.txtPatientName, tblPatient.txtPatientSurname,tblTreatmentType.txtTreatmentTypeName
				From tblTreatmentSet ,tblTreatmentVisit,tblPatient,tblTreatmentType
				where tblTreatmentSet.intTreatmentSetId = tblTreatmentVisit.intTreatmentSetId and 
					tblTreatmentSet.intPatientId = tblPatient.intPatientId and 
					tblTreatmentSet.intTreatmentTypeId= tblTreatmentType.intTreatmentTypeId
					and txtTreatmentSetRoom = {number}
			"""
		)
		return [("Дата проведения","Фамилия","Имя","Отчество","Вид процедуры")] + [i for i in cursor]
	def get_all_cab():
		cursor.execute('''SELECT DISTINCT txtTreatmentSetRoom FROM tblTreatmentSet''')
		return sorted([i[0] for i in cursor],key=lambda x:int(x))

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
		data = [ list([Paragraph(j,styles["BodyText"]) for j in i]) for i in data]
		t = Table(data)
		t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))
		for each in range(len(data)):
		    if each % 2 == 0:bg_color = colors.whitesmoke
		    else:bg_color = colors.lightgrey
		    t.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))
		document.append(t)

	#Основной цикл
	count = 0 
	for cab in get_all_cab():
		printf(f"Кабинет №{cab}")

		data = get_for_cab(cab)
		add_table(data)
		tmp_count = len(data)-1

		printf(f"Процедур в кабинете {tmp_count}")
		printf("-"*68)
		count+=tmp_count
	printf(f"Процедур всего {count}")

	SimpleDocTemplate("Работа кабинетов.pdf",title='Работа кабинетов').build(document)
	print("Отчет напечатан")





















# canv.save()