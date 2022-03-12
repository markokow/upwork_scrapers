import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import glob

extension = 'pdf'
data = glob.glob('*.{}'.format(extension))


output_folder_path = os.path.join(os.getcwd(), 'Output')
max_num = 200

if not(os.path.exists(output_folder_path)):
    os.makedirs(output_folder_path)

def splitpdf(pdf_file_path:str = ''):
    pdf = PdfFileReader(pdf_file_path)
    file_base_name = pdf_file_path.replace('.pdf', '')

    pdfWriter = PdfFileWriter()
    for page_num in range(pdf.numPages):
        
        pdfWriter.addPage(pdf.getPage(page_num))

        if (page_num+1) == pdf.numPages:
            with open(os.path.join(output_folder_path, '{0}_Page{1}.pdf'.format(file_base_name, page_num+1)), 'wb') as f:
                pdfWriter.write(f)
                f.close()
            break

        if (page_num+1) % max_num == 0:
            with open(os.path.join(output_folder_path, '{0}_Page{1}.pdf'.format(file_base_name, page_num+1)), 'wb') as f:
                pdfWriter.write(f)
                f.close()
            pdfWriter = PdfFileWriter()
        else:
            continue



for dat in data:
    print(dat)
    splitpdf(pdf_file_path=dat)