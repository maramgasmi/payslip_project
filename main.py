from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
import os


Base.metadata.create_all(bind=engine)
app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    

@app.post("/payslips/", response_model=dict)
def create_payslip(payslip:dict, db: Session = Depends(get_db)):
    import schemas, crud
    payslip_obj = schemas.PayslipCreate(**payslip)
    return crud.create_payslip(db, payslip_obj)

@app.get("/payslips/{id}", response_model=dict)
def read_payslip(id: int, db: Session = Depends(get_db)):
    import crud 
    db_payslip = crud.get_payslip(db,id)
    if not db_payslip:
        raise HTTPException(status_code=404, detail="Payslip not found ")
    return db_payslip

@app.get("/payslips/")
def read_all(db: Session = Depends(get_db)):
    import crud
    import schemas
    payslips = crud.get_all_payslips(db)
    return [schemas.PayslipResponse.from_orm(p) for p in payslips]

@app.delete("/payslips/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    import crud 
    success = crud.delete_payslip(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Payslip not found")
    return{"message": "payslip deleted "}


@app.put("/payslips/{id}")
def update(id: int, payslip: dict, db: Session = Depends(get_db)):
    import crud 
    import schemas
    payslip_obj = schemas.PayslipCreate(**payslip)
    updated = crud.update_payslip(db, id, payslip_obj)
    
    if not updated:
        raise HTTPException(status_code=404, detail="Payslip not found")
    return updated

def generate_pdf(payslip_data):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("payslip_template.html")
    html_content = template.render(**payslip_data)

    pdf_path = f"payslip_{payslip_data['id']}.pdf"

    # Write the PDF file
    with open(pdf_path, "w+b") as pdf_file:
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)

    if pisa_status.err:
        raise Exception("PDF generation failed")

    return pdf_path