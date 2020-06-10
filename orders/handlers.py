import fitz
from fpdf import FPDF, HTMLMixin


# Конвертор файлов
def convert_pdf_to_bnp(infile, outfile):
    doc = fitz.open(infile)
    page = doc.loadPage(0)
    pix = page.getPixmap()
    output = outfile
    pix.writePNG(output)


# Создатель PDF заказа
def create_order_pdf(image_path, data, image_name, spacing=1):

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font("DejaVu", size=12)
    pdf.add_page()
    text = "Automatic order form 'CRISPY MACHINE'"

    pdf.cell(200, 10, txt=text, ln=1, align="C")
    pdf.image(image_path, x=60, y=20, w=100, type='', link='')
    pdf.ln(150)  # ниже на 100
    col_width = pdf.w / 2.2
    row_height = 2 * pdf.font_size
    for row in data:
        for item in row:
            if len(item) < 36:
                pdf.cell(col_width, row_height * spacing,
                         txt=item, border=1)
            else:
                pdf.multi_cell(col_width, row_height * spacing,
                         txt=item, border=1)

        pdf.ln(row_height * spacing)
    text2 = "© 2020 Copyright: 'CRISPY MACHINE'"
    pdf.cell(200, 10, txt=text2, ln=1, align="C")
    im_name = image_name[:-3]
    im_name2 = im_name + 'PDF'
    im_name2 = im_name2.replace('C:/PP/ORP/ORP_site/OR/media/image_preview/', '')
    pdf_path = 'C:/PP/ORP/ORP_site/OR/media/temp/' + im_name2
    pdf.output(pdf_path)
    return pdf_path
