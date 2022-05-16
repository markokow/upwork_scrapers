from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

def PDF_merger(pdf_list,output_path):
    merger = PdfFileMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()

def PDF_croper(input_path,s,e,output_path):
    pdf = PdfFileReader(input_path,"rb")
    pdf_writer = PdfFileWriter()
    if s==None:
        s=1
    if e==None:
        e=pdf.getNumPages()
    
    for page in range(s-1,e):
        pdf_writer.addPage(pdf.getPage(page))

    with open(output_path,'wb') as out:
        pdf_writer.write(out)