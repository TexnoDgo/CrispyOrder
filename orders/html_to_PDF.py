from fpdf import FPDF, HTMLMixin
from fpdf import fpdf
import os

fpdf.set_global("SYSTEM_TTFONTS", os.path.join(os.path.dirname(__file__), 'fonts'))
'''pdf = fpdf.FPDF()
pdf.add_font("NotoSans", style="", fname="NotoSans-Regular.ttf", uni=True)
pdf.add_font("NotoSans", style="B", fname="NotoSans-Bold.ttf", uni=True)
pdf.add_font("NotoSans", style="I", fname="NotoSans-Italic.ttf", uni=True)
pdf.add_font("NotoSans", style="BI", fname="NotoSans-BoldItalic.ttf", uni=True)



class HTML2PDF(FPDF, HTMLMixin):
    pass
'''

data = [['First Name', 'имя'],
        ['Mike', 'Driscoll'],
        ['John', 'Doe'],
        ['Nina', 'Ma'],
        ]


def create_order_pdf(image_path, date, spacing=1):

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font("DejaVu", size=12)
    pdf.add_page()
    text = "Automatic order form 'CRISPY MACHINE'"

    #decode_text = text.encode('latin-1', 'replace').decode('cp866')
    #pdf.cell(200, 10, txt=decode_text, ln=1, align="C")
    pdf.cell(200, 10, txt=text, ln=1, align="C")
    pdf.image(image_path, x=60, y=20, w=100, type='', link='')
    pdf.ln(100)  # ниже на 85

    col_width = pdf.w / 4.5
    row_height = pdf.font_size
    for row in data:
        for item in row:
            #decode_item = item.encode('latin-1', 'replace').decode('cp866')
            pdf.cell(col_width, row_height * spacing,
                     txt=item, border=1)
        pdf.ln(row_height * spacing)
    pdf.output("PDF_order.pdf")


file_path = 'C:/PP/ORP/ORP_site/OR/media/image_preview/default.jpg'
if __name__ == '__main__':
    create_order_pdf(file_path, data)
