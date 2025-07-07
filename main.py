from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud   
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    

@app.post("/payslips/", response_model=schemas.PayslipResponse)
def create_payslip(payslip: schemas.PayslipCreate, db: Session = Depends(get_db)):
    return crud.create_payslip(db, payslip)

@app.get("/payslips/{id}", response_model=schemas.PayslipResponse)
def read_payslip(id: int, db: Session = Depends(get_db)):
    db_payslip = crud.get_payslip(db,id)
    if not db_payslip:
        raise HTTPException(status_code=404, detail="Payslip not found ")
    return db_payslip

@app.get("/payslips/", response_model=list[schemas.PayslipResponse])
def read_all(db: Session = Depends(get_db)):
    return crud.get_all_payslips(db)

@app.delete("/payslips/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    success = crud.delete_payslip(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Payslip not found")
    return{"message": "payslip deleted "}
