import pandas as pd
from fpdf import FPDF
import glob
import pathlib
import os


def generate_invoice_pdf(excel_dir_path, pdf_dir_path, img_path):
    """
    This package concverts the excel invoices to pdf invoices
    """
    filepaths = glob.glob(f"{excel_dir_path}/*.xlsx")
    print(filepaths)
    for filepath in filepaths:
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        filepath = pathlib.Path(filepath)
        filename = filepath.stem
        invoice_num, date = filename.split("-")

        pdf.set_font(family="Times", style="B", size=16)
        pdf.cell(w=0, h=8, txt=f"Invoice nr. {invoice_num}", ln=1)
        pdf.cell(w=0, h=8, txt=f"Date {date}", ln=1)
        pdf.ln(3)

        df = pd.read_excel(filepath, sheet_name="Sheet 1")
        headers = df.columns
        headers_txt = [head.replace("_", " ").title().strip() for head in headers]
        pdf.set_font(family="Times", style="B", size=10)
        pdf.cell(w=30, h=8, txt=headers_txt[0], border=1)
        pdf.cell(w=70, h=8, txt=headers_txt[1], border=1)
        pdf.cell(w=32, h=8, txt=headers_txt[2], border=1)
        pdf.cell(w=30, h=8, txt=headers_txt[3], border=1)
        pdf.cell(w=30, h=8, txt=headers_txt[4], border=1, ln=1)

        pdf.set_font(family="Times", size=10)
        for index, row in df.iterrows():
            pdf.cell(w=30, h=8, txt=str(row[headers[0]]), border=1)
            pdf.cell(w=70, h=8, txt=str(row[headers[1]]), border=1)
            pdf.cell(w=32, h=8, txt=str(row[headers[2]]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[headers[3]]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[headers[4]]), border=1, ln=1)

        total_amount = df[headers[4]].sum()

        pdf.cell(w=30, h=8, border=1)
        pdf.cell(w=70, h=8, border=1)
        pdf.cell(w=32, h=8, border=1)
        pdf.cell(w=30, h=8, border=1)
        pdf.cell(w=30, h=8, txt=str(total_amount), border=1, ln=1)

        pdf.ln(12)
        pdf.set_font(family="Times",  style="B", size=10)
        pdf.cell(w=0, h=8, txt=f"The total due amount is {total_amount} Euros.", ln=1)

        pdf.set_font(family="Times", style="B", size=16)
        pdf.cell(w=0, h=8, txt="PythonHow")
        pdf.image(img_path, x=40, w=8)
        print(1)
        if not os.path.exists(pdf_dir_path):
            os.mkdir(pdf_dir_path)
        pdf.output(f"{pdf_dir_path}/{filename}.pdf")