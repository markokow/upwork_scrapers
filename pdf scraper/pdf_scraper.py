import pdfplumber
import pandas as pd


file = 'test.pdf'

with pdfplumber.open(file) as pdf:
     page = pdf.pages[0]  
     text = page.extract_text()

print(text)