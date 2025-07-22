from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
import os


def generate_pdf(payslip_data):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("payslip_template.html")
    html_content = template.render(**payslip_data)
    pdf_path = f"payslip_{payslip_data['id']}.pdf"
    with open(pdf_path, "w+b") as pdf_file:
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)

    if pisa_status.err:
        raise Exception("PDF generation failed")

    return pdf_path