from sqlalchemy.orm import Session
import models, schemas

def create_payslip (db: Session, payslip: schemas.PayslipCreate):
    db_payslip= models.Payslip(**payslip.dict())
    db.add(db_payslip)
    db.commit()
    db.refresh(db_payslip)
    return db_payslip

def get_payslip(db: Session, payslip_id: int ):
    return db.query(models.Payslip).filter(models.Payslip.id == payslip_id).first()

def get_all_payslips(db: Session):
    return db.query(models.Payslip).all()
 

def delete_payslip(db: Session, payslip_id: int):
    db_payslip = db.query(models.Payslip).filter(models.Payslip.id== payslip_id).first()
    if db_payslip:
        db.delete(db_payslip)
        db.commit()
        return True 
    return False