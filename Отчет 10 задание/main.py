from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont #Import font
from db import data_
#C:\ProgramData\Anaconda3\Lib\site-packages\reportlab\lib

COUNT = 15

pdfmetrics.registerFont(TTFont('Bitter-Regular','Bitter-Regular.ttf', 'UTF-8')) #Register font

styles = getSampleStyleSheet()
style = styles["BodyText"]
styles['BodyText'].fontName='Bitter-Regular'

canv = Canvas("Работа кабинетов.pdf", pagesize=letter)

for cab in data_:
	aW = 500
	aH = 720
	header = Paragraph(f"<bold><font size=14>Кабинет №{cab}</font></bold>", style)
	w, h = header.wrap(aW, aH)
	aH = aH - h
	header.drawOn(canv, 72, aH)
	data_srez  = [ list([Paragraph(j,styles["BodyText"]) for j in i]) for i in data_[cab]]
	count = len(data_srez)
	last = True
	while(len(data_srez)>=COUNT or last):
		date = data_srez[0:min(COUNT,len(data_srez))]
		data_srez = data_srez[min(COUNT,len(data_srez)):]	
		last = len(date)==COUNT
		if(len(date)==0):
			
			break

		t = Table(date)
		t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
		        				('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))
		for each in range(len(date)):
		    if each % 2 == 0:
		        bg_color = colors.whitesmoke
		    else:
		        bg_color = colors.lightgrey
		    t.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))
		w, h = t.wrap(aW, aH)
		t.drawOn(canv, 52, aH-h-20)

		if(last== False or len(data_srez)==0):
			count_ = Paragraph(f"<bold><font size=14>Всего в кабинете:{count}</font></bold>", style)
			count_.wrap(aW, aH)
			count_.drawOn(canv, 52, 20)
		canv.showPage()
canv.save()